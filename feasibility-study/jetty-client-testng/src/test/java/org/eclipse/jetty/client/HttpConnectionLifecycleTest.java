//
//  ========================================================================
//  Copyright (c) 1995-2016 Mort Bay Consulting Pty. Ltd.
//  ------------------------------------------------------------------------
//  All rights reserved. This program and the accompanying materials
//  are made available under the terms of the Eclipse Public License v1.0
//  and Apache License v2.0 which accompanies this distribution.
//
//      The Eclipse Public License is available at
//      http://www.eclipse.org/legal/epl-v10.html
//
//      The Apache License v2.0 is available at
//      http://www.opensource.org/licenses/apache2.0.php
//
//  You may elect to redistribute this code under either of these licenses.
//  ========================================================================
//

package org.eclipse.jetty.client;

import org.testng.annotations.Factory;
import org.testng.annotations.Test;
import org.testng.AssertJUnit;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.util.Arrays;
import java.util.Queue;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.eclipse.jetty.client.api.Connection;
import org.eclipse.jetty.client.api.ContentResponse;
import org.eclipse.jetty.client.api.Request;
import org.eclipse.jetty.client.api.Response;
import org.eclipse.jetty.client.api.Result;
import org.eclipse.jetty.client.http.HttpDestinationOverHTTP;
import org.eclipse.jetty.client.util.ByteBufferContentProvider;
import org.eclipse.jetty.http.HttpHeader;
import org.eclipse.jetty.http.HttpVersion;
import org.eclipse.jetty.server.Handler;
import org.eclipse.jetty.server.handler.AbstractHandler;
import org.eclipse.jetty.toolchain.test.annotation.Slow;
import org.eclipse.jetty.util.log.Log;
import org.eclipse.jetty.util.log.StacklessLogging;
import org.eclipse.jetty.util.ssl.SslContextFactory;

public class HttpConnectionLifecycleTest extends AbstractHttpClientServerTest
{
	@Factory(dataProvider="parameters")
    public HttpConnectionLifecycleTest(SslContextFactory sslContextFactory)
    {
        super(sslContextFactory);
    }

    @Override
    public void start(Handler handler) throws Exception
    {
        super.start(handler);
        client.setStrictEventOrdering(false);
    }

    @Test
    public void test_SuccessfulRequest_ReturnsConnection() throws Exception
    {
        start(new EmptyServerHandler());

        String host = "localhost";
        int port = connector.getLocalPort();
        HttpDestinationOverHTTP destination = (HttpDestinationOverHTTP)client.getDestination(scheme, host, port);
        DuplexConnectionPool connectionPool = destination.getConnectionPool();

        final Queue<Connection> idleConnections = connectionPool.getIdleConnections();
        AssertJUnit.assertEquals(0, idleConnections.size());

        final Queue<Connection> activeConnections = connectionPool.getActiveConnections();
        AssertJUnit.assertEquals(0, activeConnections.size());

        final CountDownLatch headersLatch = new CountDownLatch(1);
        final CountDownLatch successLatch = new CountDownLatch(3);
        client.newRequest(host, port)
                .scheme(scheme)
                .onRequestSuccess(new Request.SuccessListener()
                {
                    @Override
                    public void onSuccess(Request request)
                    {
                        successLatch.countDown();
                    }
                })
                .onResponseHeaders(new Response.HeadersListener()
                {
                    @Override
                    public void onHeaders(Response response)
                    {
                        AssertJUnit.assertEquals(0, idleConnections.size());
                        AssertJUnit.assertEquals(1, activeConnections.size());
                        headersLatch.countDown();
                    }
                })
                .send(new Response.Listener.Adapter()
                {
                    @Override
                    public void onSuccess(Response response)
                    {
                        successLatch.countDown();
                    }

                    @Override
                    public void onComplete(Result result)
                    {
                        AssertJUnit.assertFalse(result.isFailed());
                        successLatch.countDown();
                    }
                });

        AssertJUnit.assertTrue(headersLatch.await(5, TimeUnit.SECONDS));
        AssertJUnit.assertTrue(successLatch.await(5, TimeUnit.SECONDS));

        AssertJUnit.assertEquals(1, idleConnections.size());
        AssertJUnit.assertEquals(0, activeConnections.size());
    }

    @Test
    public void test_FailedRequest_RemovesConnection() throws Exception
    {
        start(new EmptyServerHandler());

        String host = "localhost";
        int port = connector.getLocalPort();
        HttpDestinationOverHTTP destination = (HttpDestinationOverHTTP)client.getDestination(scheme, host, port);
        DuplexConnectionPool connectionPool = destination.getConnectionPool();

        final Queue<Connection> idleConnections = connectionPool.getIdleConnections();
        AssertJUnit.assertEquals(0, idleConnections.size());

        final Queue<Connection> activeConnections = connectionPool.getActiveConnections();
        AssertJUnit.assertEquals(0, activeConnections.size());

        final CountDownLatch beginLatch = new CountDownLatch(1);
        final CountDownLatch failureLatch = new CountDownLatch(2);
        client.newRequest(host, port).scheme(scheme).listener(new Request.Listener.Adapter()
        {
            @Override
            public void onBegin(Request request)
            {
                activeConnections.peek().close();
                beginLatch.countDown();
            }

            @Override
            public void onFailure(Request request, Throwable failure)
            {
                failureLatch.countDown();
            }
        }).send(new Response.Listener.Adapter()
        {
            @Override
            public void onComplete(Result result)
            {
                AssertJUnit.assertTrue(result.isFailed());
                AssertJUnit.assertEquals(0, idleConnections.size());
                AssertJUnit.assertEquals(0, activeConnections.size());
                failureLatch.countDown();
            }
        });

        AssertJUnit.assertTrue(beginLatch.await(5, TimeUnit.SECONDS));
        AssertJUnit.assertTrue(failureLatch.await(5, TimeUnit.SECONDS));

        AssertJUnit.assertEquals(0, idleConnections.size());
        AssertJUnit.assertEquals(0, activeConnections.size());
    }

    @Test
    public void test_BadRequest_RemovesConnection() throws Exception
    {
        start(new EmptyServerHandler());

        String host = "localhost";
        int port = connector.getLocalPort();
        HttpDestinationOverHTTP destination = (HttpDestinationOverHTTP)client.getDestination(scheme, host, port);
        DuplexConnectionPool connectionPool = destination.getConnectionPool();

        final Queue<Connection> idleConnections = connectionPool.getIdleConnections();
        AssertJUnit.assertEquals(0, idleConnections.size());

        final Queue<Connection> activeConnections = connectionPool.getActiveConnections();
        AssertJUnit.assertEquals(0, activeConnections.size());

        final CountDownLatch successLatch = new CountDownLatch(3);
        client.newRequest(host, port)
                .scheme(scheme)
                .listener(new Request.Listener.Adapter()
                {
                    @Override
                    public void onBegin(Request request)
                    {
                        // Remove the host header, this will make the request invalid
                        request.header(HttpHeader.HOST, null);
                    }

                    @Override
                    public void onSuccess(Request request)
                    {
                        successLatch.countDown();
                    }
                })
                .send(new Response.Listener.Adapter()
                {
                    @Override
                    public void onSuccess(Response response)
                    {
                        AssertJUnit.assertEquals(400, response.getStatus());
                        // 400 response also come with a Connection: close,
                        // so the connection is closed and removed
                        successLatch.countDown();
                    }

                    @Override
                    public void onComplete(Result result)
                    {
                        AssertJUnit.assertFalse(result.isFailed());
                        successLatch.countDown();
                    }
                });

        AssertJUnit.assertTrue(successLatch.await(5, TimeUnit.SECONDS));

        AssertJUnit.assertEquals(0, idleConnections.size());
        AssertJUnit.assertEquals(0, activeConnections.size());
    }

    @Slow
    @Test
    public void test_BadRequest_WithSlowRequest_RemovesConnection() throws Exception
    {
        start(new EmptyServerHandler());

        String host = "localhost";
        int port = connector.getLocalPort();
        HttpDestinationOverHTTP destination = (HttpDestinationOverHTTP)client.getDestination(scheme, host, port);
        DuplexConnectionPool connectionPool = destination.getConnectionPool();

        final Queue<Connection> idleConnections = connectionPool.getIdleConnections();
        AssertJUnit.assertEquals(0, idleConnections.size());

        final Queue<Connection> activeConnections = connectionPool.getActiveConnections();
        AssertJUnit.assertEquals(0, activeConnections.size());

        final long delay = 1000;
        final CountDownLatch successLatch = new CountDownLatch(3);
        client.newRequest(host, port)
                .scheme(scheme)
                .listener(new Request.Listener.Adapter()
                {
                    @Override
                    public void onBegin(Request request)
                    {
                        // Remove the host header, this will make the request invalid
                        request.header(HttpHeader.HOST, null);
                    }

                    @Override
                    public void onHeaders(Request request)
                    {
                        try
                        {
                            TimeUnit.MILLISECONDS.sleep(delay);
                        }
                        catch (InterruptedException e)
                        {
                            e.printStackTrace();
                        }
                    }

                    @Override
                    public void onSuccess(Request request)
                    {
                        successLatch.countDown();
                    }
                })
                .send(new Response.Listener.Adapter()
                {
                    @Override
                    public void onSuccess(Response response)
                    {
                        AssertJUnit.assertEquals(400, response.getStatus());
                        // 400 response also come with a Connection: close,
                        // so the connection is closed and removed
                        successLatch.countDown();
                    }

                    @Override
                    public void onComplete(Result result)
                    {
                        AssertJUnit.assertFalse(result.isFailed());
                        successLatch.countDown();
                    }
                });

        AssertJUnit.assertTrue(successLatch.await(delay * 5, TimeUnit.MILLISECONDS));

        AssertJUnit.assertEquals(0, idleConnections.size());
        AssertJUnit.assertEquals(0, activeConnections.size());
    }

    @Test
    public void test_ConnectionFailure_RemovesConnection() throws Exception
    {
        start(new EmptyServerHandler());

        String host = "localhost";
        int port = connector.getLocalPort();
        HttpDestinationOverHTTP destination = (HttpDestinationOverHTTP)client.getDestination(scheme, host, port);
        DuplexConnectionPool connectionPool = destination.getConnectionPool();

        final Queue<Connection> idleConnections = connectionPool.getIdleConnections();
        AssertJUnit.assertEquals(0, idleConnections.size());

        final Queue<Connection> activeConnections = connectionPool.getActiveConnections();
        AssertJUnit.assertEquals(0, activeConnections.size());

        server.stop();

        final CountDownLatch failureLatch = new CountDownLatch(2);
        client.newRequest(host, port)
                .scheme(scheme)
                .onRequestFailure(new Request.FailureListener()
                {
                    @Override
                    public void onFailure(Request request, Throwable failure)
                    {
                        failureLatch.countDown();
                    }
                })
                .send(new Response.Listener.Adapter()
                {
                    @Override
                    public void onComplete(Result result)
                    {
                        AssertJUnit.assertTrue(result.isFailed());
                        failureLatch.countDown();
                    }
                });

        AssertJUnit.assertTrue(failureLatch.await(5, TimeUnit.SECONDS));

        AssertJUnit.assertEquals(0, idleConnections.size());
        AssertJUnit.assertEquals(0, activeConnections.size());
    }

    @Test
    public void test_ResponseWithConnectionCloseHeader_RemovesConnection() throws Exception
    {
        start(new AbstractHandler()
        {
            @Override
            public void handle(String target, org.eclipse.jetty.server.Request baseRequest, HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException
            {
                response.setHeader("Connection", "close");
                baseRequest.setHandled(true);
            }
        });

        String host = "localhost";
        int port = connector.getLocalPort();
        HttpDestinationOverHTTP destination = (HttpDestinationOverHTTP)client.getDestination(scheme, host, port);
        DuplexConnectionPool connectionPool = destination.getConnectionPool();

        final Queue<Connection> idleConnections = connectionPool.getIdleConnections();
        AssertJUnit.assertEquals(0, idleConnections.size());

        final Queue<Connection> activeConnections = connectionPool.getActiveConnections();
        AssertJUnit.assertEquals(0, activeConnections.size());

        final CountDownLatch latch = new CountDownLatch(1);
        client.newRequest(host, port)
                .scheme(scheme)
                .send(new Response.Listener.Adapter()
                {
                    @Override
                    public void onComplete(Result result)
                    {
                        AssertJUnit.assertFalse(result.isFailed());
                        AssertJUnit.assertEquals(0, idleConnections.size());
                        AssertJUnit.assertEquals(0, activeConnections.size());
                        latch.countDown();
                    }
                });

        AssertJUnit.assertTrue(latch.await(5, TimeUnit.SECONDS));

        AssertJUnit.assertEquals(0, idleConnections.size());
        AssertJUnit.assertEquals(0, activeConnections.size());
    }

    @Test
    public void test_BigRequestContent_ResponseWithConnectionCloseHeader_RemovesConnection() throws Exception
    {
        try (StacklessLogging stackless = new StacklessLogging(HttpConnection.class))
        {
            start(new AbstractHandler()
            {
                @Override
                public void handle(String target, org.eclipse.jetty.server.Request baseRequest, HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException
                {
                    response.setHeader("Connection", "close");
                    baseRequest.setHandled(true);
                    // Don't read request content; this causes the server parser to be closed
                }
            });

            String host = "localhost";
            int port = connector.getLocalPort();
            HttpDestinationOverHTTP destination = (HttpDestinationOverHTTP)client.getDestination(scheme, host, port);
            DuplexConnectionPool connectionPool = destination.getConnectionPool();

            final Queue<Connection> idleConnections = connectionPool.getIdleConnections();
            AssertJUnit.assertEquals(0, idleConnections.size());

            final Queue<Connection> activeConnections = connectionPool.getActiveConnections();
            AssertJUnit.assertEquals(0, activeConnections.size());

            Log.getLogger(HttpConnection.class).info("Expecting java.lang.IllegalStateException: HttpParser{s=CLOSED,...");

            final CountDownLatch latch = new CountDownLatch(1);
            ByteBuffer buffer = ByteBuffer.allocate(16 * 1024 * 1024);
            Arrays.fill(buffer.array(),(byte)'x');
            client.newRequest(host, port)
                    .scheme(scheme)
                    .content(new ByteBufferContentProvider(buffer))
                    .send(new Response.Listener.Adapter()
                    {
                        @Override
                        public void onComplete(Result result)
                        {
                            AssertJUnit.assertEquals(1, latch.getCount());
                            AssertJUnit.assertEquals(0, idleConnections.size());
                            AssertJUnit.assertEquals(0, activeConnections.size());
                            latch.countDown();
                        }
                    });

            AssertJUnit.assertTrue(latch.await(5, TimeUnit.SECONDS));

            AssertJUnit.assertEquals(0, idleConnections.size());
            AssertJUnit.assertEquals(0, activeConnections.size());

            server.stop();
        }
    }

    @Slow
    @Test
    public void test_IdleConnection_IsClosed_OnRemoteClose() throws Exception
    {
        start(new EmptyServerHandler());

        String host = "localhost";
        int port = connector.getLocalPort();
        HttpDestinationOverHTTP destination = (HttpDestinationOverHTTP)client.getDestination(scheme, host, port);
        DuplexConnectionPool connectionPool = destination.getConnectionPool();

        final Queue<Connection> idleConnections = connectionPool.getIdleConnections();
        AssertJUnit.assertEquals(0, idleConnections.size());

        final Queue<Connection> activeConnections = connectionPool.getActiveConnections();
        AssertJUnit.assertEquals(0, activeConnections.size());

        ContentResponse response = client.newRequest(host, port)
                .scheme(scheme)
                .timeout(5, TimeUnit.SECONDS)
                .send();

        AssertJUnit.assertEquals(200, response.getStatus());

        connector.stop();

        // Give the connection some time to process the remote close
        TimeUnit.SECONDS.sleep(1);

        AssertJUnit.assertEquals(0, idleConnections.size());
        AssertJUnit.assertEquals(0, activeConnections.size());
    }

    @Test
    public void testConnectionForHTTP10ResponseIsRemoved() throws Exception
    {
        start(new EmptyServerHandler());

        String host = "localhost";
        int port = connector.getLocalPort();
        HttpDestinationOverHTTP destination = (HttpDestinationOverHTTP)client.getDestination(scheme, host, port);
        DuplexConnectionPool connectionPool = destination.getConnectionPool();

        final Queue<Connection> idleConnections = connectionPool.getIdleConnections();
        AssertJUnit.assertEquals(0, idleConnections.size());

        final Queue<Connection> activeConnections = connectionPool.getActiveConnections();
        AssertJUnit.assertEquals(0, activeConnections.size());

        client.setStrictEventOrdering(false);
        ContentResponse response = client.newRequest(host, port)
                .scheme(scheme)
                .onResponseBegin(new Response.BeginListener()
                {
                    @Override
                    public void onBegin(Response response)
                    {
                        // Simulate a HTTP 1.0 response has been received.
                        ((HttpResponse)response).version(HttpVersion.HTTP_1_0);
                    }
                })
                .send();

        AssertJUnit.assertEquals(200, response.getStatus());

        AssertJUnit.assertEquals(0, idleConnections.size());
        AssertJUnit.assertEquals(0, activeConnections.size());
    }
}
