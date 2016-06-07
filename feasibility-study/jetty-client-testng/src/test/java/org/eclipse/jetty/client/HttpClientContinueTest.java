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
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import javax.servlet.ServletException;
import javax.servlet.ServletInputStream;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.eclipse.jetty.client.api.ContentResponse;
import org.eclipse.jetty.client.api.Response;
import org.eclipse.jetty.client.api.Result;
import org.eclipse.jetty.client.util.BufferingResponseListener;
import org.eclipse.jetty.client.util.BytesContentProvider;
import org.eclipse.jetty.client.util.DeferredContentProvider;
import org.eclipse.jetty.http.HttpHeader;
import org.eclipse.jetty.http.HttpHeaderValue;
import org.eclipse.jetty.http.HttpMethod;
import org.eclipse.jetty.server.Request;
import org.eclipse.jetty.server.handler.AbstractHandler;
import org.eclipse.jetty.toolchain.test.annotation.Slow;
import org.eclipse.jetty.util.IO;
import org.eclipse.jetty.util.ssl.SslContextFactory;

public class HttpClientContinueTest extends AbstractHttpClientServerTest
{
	@Factory(dataProvider="parameters")
    public HttpClientContinueTest(SslContextFactory sslContextFactory)
    {
        super(sslContextFactory);
    }

    @Test
    public void test_Expect100Continue_WithOneContent_Respond100Continue() throws Exception
    {
        test_Expect100Continue_Respond100Continue("data1".getBytes(StandardCharsets.UTF_8));
    }

    @Test
    public void test_Expect100Continue_WithMultipleContents_Respond100Continue() throws Exception
    {
        test_Expect100Continue_Respond100Continue("data1".getBytes(StandardCharsets.UTF_8), "data2".getBytes(StandardCharsets.UTF_8), "data3".getBytes(StandardCharsets.UTF_8));
    }

    @Test(enabled = false)
	private void test_Expect100Continue_Respond100Continue(byte[]... contents) throws Exception
    {
        start(new AbstractHandler()
        {
            @Override
            public void handle(String target, Request baseRequest, HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException
            {
                baseRequest.setHandled(true);
                // Send 100-Continue and copy the content back
                IO.copy(request.getInputStream(), response.getOutputStream());
            }
        });

        ContentResponse response = client.newRequest("localhost", connector.getLocalPort())
                .scheme(scheme)
                .header(HttpHeader.EXPECT, HttpHeaderValue.CONTINUE.asString())
                .content(new BytesContentProvider(contents))
                .timeout(5, TimeUnit.SECONDS)
                .send();

        AssertJUnit.assertNotNull(response);
        AssertJUnit.assertEquals(200, response.getStatus());

        int index = 0;
        byte[] responseContent = response.getContent();
        for (byte[] content : contents)
        {
            for (byte b : content)
            {
                AssertJUnit.assertEquals(b, responseContent[index++]);
            }
        }
    }

    @Test
    public void test_Expect100Continue_WithChunkedContent_Respond100Continue() throws Exception
    {
        start(new AbstractHandler()
        {
            @Override
            public void handle(String target, Request baseRequest, HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException
            {
                baseRequest.setHandled(true);
                // Send 100-Continue and copy the content back
                ServletInputStream input = request.getInputStream();
                // Make sure we chunk the response too
                response.flushBuffer();
                IO.copy(input, response.getOutputStream());
            }
        });

        byte[] content1 = new byte[10240];
        byte[] content2 = new byte[16384];
        ContentResponse response = client.newRequest("localhost", connector.getLocalPort())
                .scheme(scheme)
                .header(HttpHeader.EXPECT, HttpHeaderValue.CONTINUE.asString())
                .content(new BytesContentProvider(content1, content2)
                {
                    @Override
                    public long getLength()
                    {
                        return -1;
                    }
                })
                .timeout(5, TimeUnit.SECONDS)
                .send();

        AssertJUnit.assertNotNull(response);
        AssertJUnit.assertEquals(200, response.getStatus());

        int index = 0;
        byte[] responseContent = response.getContent();
        for (byte b : content1)
            AssertJUnit.assertEquals(b, responseContent[index++]);
        for (byte b : content2)
            AssertJUnit.assertEquals(b, responseContent[index++]);
    }

    @Test
    public void test_Expect100Continue_WithContent_Respond417ExpectationFailed() throws Exception
    {
        test_Expect100Continue_WithContent_RespondError(417);
    }

    @Test
    public void test_Expect100Continue_WithContent_Respond413RequestEntityTooLarge() throws Exception
    {
        test_Expect100Continue_WithContent_RespondError(413);
    }

    @Test(enabled = false)
	private void test_Expect100Continue_WithContent_RespondError(final int error) throws Exception
    {
        start(new AbstractHandler()
        {
            @Override
            public void handle(String target, Request baseRequest, HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException
            {
                baseRequest.setHandled(true);
                response.sendError(error);
            }
        });

        byte[] content1 = new byte[10240];
        byte[] content2 = new byte[16384];
        final CountDownLatch latch = new CountDownLatch(1);
        client.newRequest("localhost", connector.getLocalPort())
                .scheme(scheme)
                .header(HttpHeader.EXPECT, HttpHeaderValue.CONTINUE.asString())
                .content(new BytesContentProvider(content1, content2))
                .send(new BufferingResponseListener()
                {
                    @Override
                    public void onComplete(Result result)
                    {
                        AssertJUnit.assertTrue(result.isFailed());
                        AssertJUnit.assertNotNull(result.getRequestFailure());
                        AssertJUnit.assertNull(result.getResponseFailure());
                        byte[] content = getContent();
                        AssertJUnit.assertNotNull(content);
                        AssertJUnit.assertTrue(content.length > 0);
                        AssertJUnit.assertEquals(error, result.getResponse().getStatus());
                        latch.countDown();
                    }
                });

        AssertJUnit.assertTrue(latch.await(5, TimeUnit.SECONDS));
    }

    @Test
    public void test_Expect100Continue_WithContent_WithRedirect() throws Exception
    {
        final String data = "success";
        start(new AbstractHandler()
        {
            @Override
            public void handle(String target, Request baseRequest, HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException
            {
                baseRequest.setHandled(true);
                if (request.getRequestURI().endsWith("/done"))
                {
                    response.getOutputStream().print(data);
                }
                else
                {
                    // Send 100-Continue and consume the content
                    IO.copy(request.getInputStream(), new ByteArrayOutputStream());
                    // Send a redirect
                    response.sendRedirect("/done");
                }
            }
        });

        byte[] content = new byte[10240];
        final CountDownLatch latch = new CountDownLatch(1);
        client.newRequest("localhost", connector.getLocalPort())
                .scheme(scheme)
                .method(HttpMethod.POST)
                .path("/continue")
                .header(HttpHeader.EXPECT, HttpHeaderValue.CONTINUE.asString())
                .content(new BytesContentProvider(content))
                .send(new BufferingResponseListener()
                {
                    @Override
                    public void onComplete(Result result)
                    {
                        AssertJUnit.assertFalse(result.isFailed());
                        AssertJUnit.assertEquals(200, result.getResponse().getStatus());
                        AssertJUnit.assertEquals(data, getContentAsString());
                        latch.countDown();
                    }
                });

        AssertJUnit.assertTrue(latch.await(5, TimeUnit.SECONDS));
    }

    @Test
    public void test_Redirect_WithExpect100Continue_WithContent() throws Exception
    {
        // A request with Expect: 100-Continue cannot receive non-final responses like 3xx

        final String data = "success";
        start(new AbstractHandler()
        {
            @Override
            public void handle(String target, Request baseRequest, HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException
            {
                baseRequest.setHandled(true);
                if (request.getRequestURI().endsWith("/done"))
                {
                    // Send 100-Continue and consume the content
                    IO.copy(request.getInputStream(), new ByteArrayOutputStream());
                    response.getOutputStream().print(data);
                }
                else
                {
                    // Send a redirect
                    response.sendRedirect("/done");
                }
            }
        });

        byte[] content = new byte[10240];
        final CountDownLatch latch = new CountDownLatch(1);
        client.newRequest("localhost", connector.getLocalPort())
                .scheme(scheme)
                .method(HttpMethod.POST)
                .path("/redirect")
                .header(HttpHeader.EXPECT, HttpHeaderValue.CONTINUE.asString())
                .content(new BytesContentProvider(content))
                .send(new BufferingResponseListener()
                {
                    @Override
                    public void onComplete(Result result)
                    {
                        AssertJUnit.assertTrue(result.isFailed());
                        AssertJUnit.assertNotNull(result.getRequestFailure());
                        AssertJUnit.assertNull(result.getResponseFailure());
                        AssertJUnit.assertEquals(302, result.getResponse().getStatus());
                        latch.countDown();
                    }
                });

        AssertJUnit.assertTrue(latch.await(5, TimeUnit.SECONDS));
    }

    @Slow
    @Test
    public void test_Expect100Continue_WithContent_WithResponseFailure_Before100Continue() throws Exception
    {
        final long idleTimeout = 1000;
        start(new AbstractHandler()
        {
            @Override
            public void handle(String target, Request baseRequest, HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException
            {
                baseRequest.setHandled(true);
                try
                {
                    TimeUnit.MILLISECONDS.sleep(2 * idleTimeout);
                }
                catch (InterruptedException x)
                {
                    throw new ServletException(x);
                }
            }
        });

        client.setIdleTimeout(idleTimeout);

        byte[] content = new byte[1024];
        final CountDownLatch latch = new CountDownLatch(1);
        client.newRequest("localhost", connector.getLocalPort())
                .scheme(scheme)
                .header(HttpHeader.EXPECT, HttpHeaderValue.CONTINUE.asString())
                .content(new BytesContentProvider(content))
                .send(new BufferingResponseListener()
                {
                    @Override
                    public void onComplete(Result result)
                    {
                        AssertJUnit.assertTrue(result.isFailed());
                        AssertJUnit.assertNotNull(result.getRequestFailure());
                        AssertJUnit.assertNotNull(result.getResponseFailure());
                        latch.countDown();
                    }
                });

        AssertJUnit.assertTrue(latch.await(3 * idleTimeout, TimeUnit.MILLISECONDS));
    }

    @Slow
    @Test
    public void test_Expect100Continue_WithContent_WithResponseFailure_After100Continue() throws Exception
    {
        final long idleTimeout = 1000;
        start(new AbstractHandler()
        {
            @Override
            public void handle(String target, Request baseRequest, HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException
            {
                baseRequest.setHandled(true);
                // Send 100-Continue and consume the content
                IO.copy(request.getInputStream(), new ByteArrayOutputStream());
                try
                {
                    TimeUnit.MILLISECONDS.sleep(2 * idleTimeout);
                }
                catch (InterruptedException x)
                {
                    throw new ServletException(x);
                }
            }
        });

        client.setIdleTimeout(idleTimeout);

        byte[] content = new byte[1024];
        final CountDownLatch latch = new CountDownLatch(1);
        client.newRequest("localhost", connector.getLocalPort())
                .scheme(scheme)
                .header(HttpHeader.EXPECT, HttpHeaderValue.CONTINUE.asString())
                .content(new BytesContentProvider(content))
                .send(new BufferingResponseListener()
                {
                    @Override
                    public void onComplete(Result result)
                    {
                        AssertJUnit.assertTrue(result.isFailed());
                        AssertJUnit.assertNull(result.getRequestFailure());
                        AssertJUnit.assertNotNull(result.getResponseFailure());
                        latch.countDown();
                    }
                });

        AssertJUnit.assertTrue(latch.await(3 * idleTimeout, TimeUnit.MILLISECONDS));
    }

    @Test
    public void test_Expect100Continue_WithContent_WithResponseFailure_During100Continue() throws Exception
    {
        start(new AbstractHandler()
        {
            @Override
            public void handle(String target, Request baseRequest, HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException
            {
                baseRequest.setHandled(true);
                // Send 100-Continue and consume the content
                IO.copy(request.getInputStream(), new ByteArrayOutputStream());
            }
        });

        client.getProtocolHandlers().clear();
        client.getProtocolHandlers().put(new ContinueProtocolHandler()
        {
            @Override
            public Response.Listener getResponseListener()
            {
                final Response.Listener listener = super.getResponseListener();
                return new Response.Listener.Adapter()
                {
                    @Override
                    public void onBegin(Response response)
                    {
                        response.abort(new Exception());
                    }

                    @Override
                    public void onFailure(Response response, Throwable failure)
                    {
                        listener.onFailure(response, failure);
                    }
                };
            }
        });

        byte[] content = new byte[1024];
        final CountDownLatch latch = new CountDownLatch(1);
        client.newRequest("localhost", connector.getLocalPort())
        .scheme(scheme)
        .header(HttpHeader.EXPECT, HttpHeaderValue.CONTINUE.asString())
        .content(new BytesContentProvider(content))
        .send(new BufferingResponseListener()
        {
            @Override
            public void onComplete(Result result)
            {
                AssertJUnit.assertTrue(result.isFailed());
                AssertJUnit.assertNotNull(result.getRequestFailure());
                AssertJUnit.assertNotNull(result.getResponseFailure());
                latch.countDown();
            }
        });

        AssertJUnit.assertTrue(latch.await(5, TimeUnit.SECONDS));
    }

    @Slow
    @Test
    public void test_Expect100Continue_WithDeferredContent_Respond100Continue() throws Exception
    {
        start(new AbstractHandler()
        {
            @Override
            public void handle(String target, Request baseRequest, HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException
            {
                baseRequest.setHandled(true);
                // Send 100-Continue and echo the content
                IO.copy(request.getInputStream(), response.getOutputStream());
            }
        });

        final byte[] chunk1 = new byte[]{0, 1, 2, 3};
        final byte[] chunk2 = new byte[]{4, 5, 6, 7};
        final byte[] data = new byte[chunk1.length + chunk2.length];
        System.arraycopy(chunk1, 0, data, 0, chunk1.length);
        System.arraycopy(chunk2, 0, data, chunk1.length, chunk2.length);

        final CountDownLatch latch = new CountDownLatch(1);
        DeferredContentProvider content = new DeferredContentProvider();
        client.newRequest("localhost", connector.getLocalPort())
                .scheme(scheme)
                .header(HttpHeader.EXPECT, HttpHeaderValue.CONTINUE.asString())
                .content(content)
                .send(new BufferingResponseListener()
                {
                    @Override
                    public void onComplete(Result result)
                    {
                        AssertJUnit.assertArrayEquals(data, getContent());
                        latch.countDown();
                    }
                });

        Thread.sleep(1000);

        content.offer(ByteBuffer.wrap(chunk1));

        Thread.sleep(1000);

        content.offer(ByteBuffer.wrap(chunk2));
        content.close();

        AssertJUnit.assertTrue(latch.await(5, TimeUnit.SECONDS));
    }

    @Slow
    @Test
    public void test_Expect100Continue_WithInitialAndDeferredContent_Respond100Continue() throws Exception
    {
        start(new AbstractHandler()
        {
            @Override
            public void handle(String target, Request baseRequest, HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException
            {
                baseRequest.setHandled(true);
                // Send 100-Continue and echo the content
                IO.copy(request.getInputStream(), response.getOutputStream());
            }
        });

        final byte[] chunk1 = new byte[]{0, 1, 2, 3};
        final byte[] chunk2 = new byte[]{4, 5, 6, 7};
        final byte[] data = new byte[chunk1.length + chunk2.length];
        System.arraycopy(chunk1, 0, data, 0, chunk1.length);
        System.arraycopy(chunk2, 0, data, chunk1.length, chunk2.length);

        final CountDownLatch latch = new CountDownLatch(1);
        DeferredContentProvider content = new DeferredContentProvider(ByteBuffer.wrap(chunk1));
        client.newRequest("localhost", connector.getLocalPort())
                .scheme(scheme)
                .header(HttpHeader.EXPECT, HttpHeaderValue.CONTINUE.asString())
                .content(content)
                .send(new BufferingResponseListener()
                {
                    @Override
                    public void onComplete(Result result)
                    {
                        AssertJUnit.assertArrayEquals(data, getContent());
                        latch.countDown();
                    }
                });

        Thread.sleep(1000);

        content.offer(ByteBuffer.wrap(chunk2));
        content.close();

        AssertJUnit.assertTrue(latch.await(5, TimeUnit.SECONDS));
    }

    @Test
    public void test_Expect100Continue_WithConcurrentDeferredContent_Respond100Continue() throws Exception
    {
        start(new AbstractHandler()
        {
            @Override
            public void handle(String target, Request baseRequest, HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException
            {
                baseRequest.setHandled(true);
                // Send 100-Continue and echo the content
                IO.copy(request.getInputStream(), response.getOutputStream());
            }
        });

        final byte[] data = new byte[]{0, 1, 2, 3, 4, 5, 6, 7};
        final DeferredContentProvider content = new DeferredContentProvider();

        final CountDownLatch latch = new CountDownLatch(1);
        client.newRequest("localhost", connector.getLocalPort())
                .scheme(scheme)
                .header(HttpHeader.EXPECT, HttpHeaderValue.CONTINUE.asString())
                .onRequestHeaders(new org.eclipse.jetty.client.api.Request.HeadersListener()
                {
                    @Override
                    public void onHeaders(org.eclipse.jetty.client.api.Request request)
                    {
                        content.offer(ByteBuffer.wrap(data));
                        content.close();
                    }
                })
                .content(content)
                .send(new BufferingResponseListener()
                {
                    @Override
                    public void onComplete(Result result)
                    {
                        AssertJUnit.assertArrayEquals(data, getContent());
                        latch.countDown();
                    }
                });

        AssertJUnit.assertTrue(latch.await(5, TimeUnit.SECONDS));
    }

    @Test
    public void test_Expect100Continue_WithInitialAndConcurrentDeferredContent_Respond100Continue() throws Exception
    {
        start(new AbstractHandler()
        {
            @Override
            public void handle(String target, Request baseRequest, HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException
            {
                baseRequest.setHandled(true);
                // Send 100-Continue and echo the content
                IO.copy(request.getInputStream(), response.getOutputStream());
            }
        });

        final byte[] chunk1 = new byte[]{0, 1, 2, 3};
        final byte[] chunk2 = new byte[]{4, 5, 6};
        final byte[] data = new byte[chunk1.length + chunk2.length];
        System.arraycopy(chunk1, 0, data, 0, chunk1.length);
        System.arraycopy(chunk2, 0, data, chunk1.length, chunk2.length);

        final DeferredContentProvider content = new DeferredContentProvider(ByteBuffer.wrap(chunk1));

        client.getProtocolHandlers().put(new ContinueProtocolHandler()
        {
            @Override
            public Response.Listener getResponseListener()
            {
                return new ContinueListener()
                {
                    @Override
                    public void onHeaders(Response response)
                    {
                        super.onHeaders(response);
                        content.offer(ByteBuffer.wrap(chunk2));
                        content.close();
                    }
                };
            }
        });

        final CountDownLatch latch = new CountDownLatch(1);
        client.newRequest("localhost", connector.getLocalPort())
                .scheme(scheme)
                .header(HttpHeader.EXPECT, HttpHeaderValue.CONTINUE.asString())
                .content(content)
                .send(new BufferingResponseListener()
                {
                    @Override
                    public void onComplete(Result result)
                    {
                        AssertJUnit.assertArrayEquals(data, getContent());
                        latch.countDown();
                    }
                });

        AssertJUnit.assertTrue(latch.await(5, TimeUnit.SECONDS));
    }

    @Test
    public void test_Expect100Continue_WithTwoResponsesInOneRead() throws Exception
    {
        // There is a chance that the server replies with the 100 Continue response
        // and immediately after with the "normal" response, say a 200 OK.
        // These may be read by the client in a single read, and must be handled correctly.

        startClient();

        try (ServerSocket server = new ServerSocket())
        {
            server.bind(new InetSocketAddress("localhost", 0));

            final CountDownLatch latch = new CountDownLatch(1);
            client.newRequest("localhost", server.getLocalPort())
                    .header(HttpHeader.EXPECT, HttpHeaderValue.CONTINUE.asString())
                    .content(new BytesContentProvider(new byte[]{0}))
                    .send(new Response.CompleteListener()
                    {
                        @Override
                        public void onComplete(Result result)
                        {
                            AssertJUnit.assertTrue(result.toString(), result.isSucceeded());
                            AssertJUnit.assertEquals(200, result.getResponse().getStatus());
                            latch.countDown();
                        }
                    });

            try (Socket socket = server.accept())
            {
                // Read the request headers.
                InputStream input = socket.getInputStream();
                int crlfs = 0;
                while (true)
                {
                    int read = input.read();
                    if (read == '\r' || read == '\n')
                        ++crlfs;
                    else
                        crlfs = 0;
                    if (crlfs == 4)
                        break;
                }

                OutputStream output = socket.getOutputStream();
                String responses = "" +
                        "HTTP/1.1 100 Continue\r\n" +
                        "\r\n" +
                        "HTTP/1.1 200 OK\r\n" +
                        "Transfer-Encoding: chunked\r\n" +
                        "\r\n" +
                        "10\r\n" +
                        "0123456789ABCDEF\r\n";
                output.write(responses.getBytes(StandardCharsets.UTF_8));
                output.flush();

                Thread.sleep(1000);

                String content = "" +
                        "10\r\n" +
                        "0123456789ABCDEF\r\n" +
                        "0\r\n" +
                        "\r\n";
                output.write(content.getBytes(StandardCharsets.UTF_8));
                output.flush();

                AssertJUnit.assertTrue(latch.await(5, TimeUnit.SECONDS));
            }
        }
    }
}
