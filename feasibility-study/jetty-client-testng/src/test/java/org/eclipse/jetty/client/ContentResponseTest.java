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
import java.util.Random;
import java.util.concurrent.TimeUnit;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.eclipse.jetty.client.api.ContentResponse;
import org.eclipse.jetty.http.HttpHeader;
import org.eclipse.jetty.server.Request;
import org.eclipse.jetty.server.handler.AbstractHandler;
import org.eclipse.jetty.util.ssl.SslContextFactory;

public class ContentResponseTest extends AbstractHttpClientServerTest
{
	@Factory(dataProvider="parameters")
    public ContentResponseTest(SslContextFactory sslContextFactory)
    {
        super(sslContextFactory);
    }

    @Test
    public void testResponseWithoutContentType() throws Exception
    {
        final byte[] content = new byte[1024];
        new Random().nextBytes(content);
        start(new AbstractHandler()
        {
            @Override
            public void handle(String target, Request baseRequest, HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException
            {
                baseRequest.setHandled(true);
                response.getOutputStream().write(content);
            }
        });

        ContentResponse response = client.newRequest("localhost", connector.getLocalPort())
                .scheme(scheme)
                .timeout(5, TimeUnit.SECONDS)
                .send();

        AssertJUnit.assertEquals(200, response.getStatus());
        AssertJUnit.assertArrayEquals(content, response.getContent());
        AssertJUnit.assertNull(response.getMediaType());
        AssertJUnit.assertNull(response.getEncoding());
    }

    @Test
    public void testResponseWithMediaType() throws Exception
    {
        final String content = "The quick brown fox jumped over the lazy dog";
        final String mediaType = "text/plain";
        start(new AbstractHandler()
        {
            @Override
            public void handle(String target, Request baseRequest, HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException
            {
                baseRequest.setHandled(true);
                response.setHeader(HttpHeader.CONTENT_TYPE.asString(), mediaType);
                response.getOutputStream().write(content.getBytes("UTF-8"));
            }
        });

        ContentResponse response = client.newRequest("localhost", connector.getLocalPort())
                .scheme(scheme)
                .timeout(5, TimeUnit.SECONDS)
                .send();

        AssertJUnit.assertEquals(200, response.getStatus());
        AssertJUnit.assertEquals(content, response.getContentAsString());
        AssertJUnit.assertEquals(mediaType, response.getMediaType());
        AssertJUnit.assertNull(response.getEncoding());
    }

    @Test
    public void testResponseWithContentType() throws Exception
    {
        final String content = "The quick brown fox jumped over the lazy dog";
        final String mediaType = "text/plain";
        final String encoding = "UTF-8";
        final String contentType = mediaType + "; charset=" + encoding;
        start(new AbstractHandler()
        {
            @Override
            public void handle(String target, Request baseRequest, HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException
            {
                baseRequest.setHandled(true);
                response.setHeader(HttpHeader.CONTENT_TYPE.asString(), contentType);
                response.getOutputStream().write(content.getBytes("UTF-8"));
            }
        });

        ContentResponse response = client.newRequest("localhost", connector.getLocalPort())
                .scheme(scheme)
                .timeout(5, TimeUnit.SECONDS)
                .send();

        AssertJUnit.assertEquals(200, response.getStatus());
        AssertJUnit.assertEquals(content, response.getContentAsString());
        AssertJUnit.assertEquals(mediaType, response.getMediaType());
        AssertJUnit.assertEquals(encoding, response.getEncoding());
    }
}
