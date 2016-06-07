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
import java.net.HttpCookie;
import java.net.URI;
import java.util.List;
import java.util.concurrent.TimeUnit;

import javax.servlet.ServletException;
import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.eclipse.jetty.client.api.ContentResponse;
import org.eclipse.jetty.client.api.Response;
import org.eclipse.jetty.server.Request;
import org.eclipse.jetty.server.handler.AbstractHandler;
import org.eclipse.jetty.util.ssl.SslContextFactory;

public class HttpCookieTest extends AbstractHttpClientServerTest
{
	@Factory(dataProvider="parameters")
    public HttpCookieTest(SslContextFactory sslContextFactory)
    {
        super(sslContextFactory);
    }

    @Test
    public void test_CookieIsStored() throws Exception
    {
        final String name = "foo";
        final String value = "bar";
        start(new AbstractHandler()
        {
            @Override
            public void handle(String target, Request baseRequest, HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException
            {
                response.addCookie(new Cookie(name, value));
                baseRequest.setHandled(true);
            }
        });

        String host = "localhost";
        int port = connector.getLocalPort();
        String path = "/path";
        String uri = scheme + "://" + host + ":" + port + path;
        Response response = client.GET(uri);
        AssertJUnit.assertEquals(200, response.getStatus());

        List<HttpCookie> cookies = client.getCookieStore().get(URI.create(uri));
        AssertJUnit.assertNotNull(cookies);
        AssertJUnit.assertEquals(1, cookies.size());
        HttpCookie cookie = cookies.get(0);
        AssertJUnit.assertEquals(name, cookie.getName());
        AssertJUnit.assertEquals(value, cookie.getValue());
    }

    @Test
    public void test_CookieIsSent() throws Exception
    {
        final String name = "foo";
        final String value = "bar";
        start(new AbstractHandler()
        {
            @Override
            public void handle(String target, Request baseRequest, HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException
            {
                baseRequest.setHandled(true);
                Cookie[] cookies = request.getCookies();
                AssertJUnit.assertNotNull(cookies);
                AssertJUnit.assertEquals(1, cookies.length);
                Cookie cookie = cookies[0];
                AssertJUnit.assertEquals(name, cookie.getName());
                AssertJUnit.assertEquals(value, cookie.getValue());
            }
        });

        String host = "localhost";
        int port = connector.getLocalPort();
        String path = "/path";
        String uri = scheme + "://" + host + ":" + port;
        HttpCookie cookie = new HttpCookie(name, value);
        client.getCookieStore().add(URI.create(uri), cookie);

        Response response = client.GET(scheme + "://" + host + ":" + port + path);
        AssertJUnit.assertEquals(200, response.getStatus());
    }

    @Test
    public void test_CookieWithoutValue() throws Exception
    {
        start(new AbstractHandler()
        {
            @Override
            public void handle(String target, Request baseRequest, HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException
            {
                baseRequest.setHandled(true);
                response.addHeader("Set-Cookie", "");
            }
        });

        ContentResponse response = client.newRequest("localhost", connector.getLocalPort())
                .scheme(scheme)
                .send();
        AssertJUnit.assertEquals(200, response.getStatus());
        AssertJUnit.assertTrue(client.getCookieStore().getCookies().isEmpty());
    }

    @Test
    public void test_PerRequestCookieIsSent() throws Exception
    {
        final String name = "foo";
        final String value = "bar";
        start(new AbstractHandler()
        {
            @Override
            public void handle(String target, Request baseRequest, HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException
            {
                baseRequest.setHandled(true);
                Cookie[] cookies = request.getCookies();
                AssertJUnit.assertNotNull(cookies);
                AssertJUnit.assertEquals(1, cookies.length);
                Cookie cookie = cookies[0];
                AssertJUnit.assertEquals(name, cookie.getName());
                AssertJUnit.assertEquals(value, cookie.getValue());
            }
        });

        ContentResponse response = client.newRequest("localhost", connector.getLocalPort())
                .scheme(scheme)
                .cookie(new HttpCookie(name, value))
                .timeout(5, TimeUnit.SECONDS)
                .send();
        AssertJUnit.assertEquals(200, response.getStatus());
    }
}
