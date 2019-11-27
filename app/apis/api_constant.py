#!/usr/bin/env python
# coding=utf-8
'''
@Description: 
@Author: Xuannan
@Date: 2019-11-21 22:03:43
@LastEditTime: 2019-11-27 22:05:13
@LastEditors: Xuannan
'''

USER_ACTION_LOGIN = 'login'
USER_ACTION_REGISTER = 'register'
USER_ACTION_CHANGE_PWD = 'change_pwd'
USER_ACTION_CHANGE_INFO = 'change_info'

class RET:
    Continue = 100
    SwitchingProtocols = 101
    OK = 200
    Created = 201
    Accepted = 202
    NonAuthoritativeInformation = 203
    NoContent = 204
    ResetContent = 205
    PartialContent = 206
    MultipleChoices = 300
    MovedPermanently = 301
    Found = 302
    SeeOther = 303
    NotModified = 304
    UseProxy=305
    Unused=306
    TemporaryRedirect=307
    BadRequest=400
    Unauthorized=401
    PaymentRequired=402
    Forbidden=403
    NotFound=404
    MethodNotAllowed=405
    NotAcceptable=406
    ProxyAuthenticationRequired=407
    RequestTimeout=408
    Conflict=409
    Gone=410
    LengthRequired=411
    PreconditionFailed=412
    RequestEntityTooLarge=413
    RequestURITooLarge=414
    UnsupportedMediaType=415
    RequestedRangeNotSatisfiable=416
    ExpectationFailed=417
    InternalServerError=500
    NoImplemented=501
    BadGateway=502
    ServiceUnavailable=503
    GatewayTimeout=504
    HTTPVersionNotSupported=505


error_map = {
    RET.Continue:'继续。客户端应继续其请求',
    RET.SwitchingProtocols:'切换协议。服务器根据客户端的请求切换协议。只能切换到更高级的协议，例如，切换到HTTP的新版本协议',
    RET.OK:'请求成功。一般用于GET与POST请求',
    RET.Created:'已创建。成功请求并创建了新的资源',
    RET.Accepted:'已接受。已经接受请求，但未处理完成',
    RET.NonAuthoritativeInformation:'非授权信息。请求成功。但返回的meta信息不在原始的服务器，而是一个副本',
    RET.NoContent:'无内容。服务器成功处理，但未返回内容。在未更新网页的情况下，可确保浏览器继续显示当前文档',
    RET.ResetContent:'重置内容。服务器处理成功，用户终端（例如：浏览器）应重置文档视图。可通过此返回码清除浏览器的表单域',
    RET.PartialContent:'部分内容。服务器成功处理了部分GET请求',
    RET.MultipleChoices:'多种选择。请求的资源可包括多个位置，相应可返回一个资源特征与地址的列表用于用户终端（例如：浏览器）选择',
    RET.MovedPermanently:'永久移动。请求的资源已被永久的移动到新URI，返回信息会包括新的URI，浏览器会自动定向到新URI。今后任何新的请求都应使用新的URI代替',
    RET.Found:'临时移动。与301类似。但资源只是临时被移动。客户端应继续使用原有URI',
    RET.SeeOther:'查看其它地址。与301类似。使用GET和POST请求查看',
    RET.NotModified:'未修改。所请求的资源未修改，服务器返回此状态码时，不会返回任何资源。客户端通常会缓存访问过的资源，通过提供一个头信息指出客户端希望只返回在指定日期之后修改的资源',
    RET.UseProxy:'使用代理。所请求的资源必须通过代理访问',
    RET.Unused:'已经被废弃的HTTP状态码',
    RET.TemporaryRedirect:'临时重定向。与302类似。使用GET请求重定向',
    RET.BadRequest:'客户端请求的语法错误，服务器无法理解',
    RET.Unauthorized:'请求要求用户的身份认证',
    RET.PaymentRequired:'保留，将来使用',
    RET.Forbidden:'服务器理解请求客户端的请求，但是拒绝执行此请求',
    RET.NotFound:'服务器无法根据客户端的请求找到资源（网页）。通过此代码，网站设计人员可设置"您所请求的资源无法找到"的个性页面',
    RET.MethodNotAllowed:'客户端请求中的方法被禁止',
    RET.NotAcceptable:'服务器无法根据客户端请求的内容特性完成请求',
    RET.ProxyAuthenticationRequired:'请求要求代理的身份认证，与401类似，但请求者应当使用代理进行授权',
    RET.RequestTimeout:'服务器等待客户端发送的请求时间过长，超时',
    RET.Conflict:'服务器完成客户端的PUT请求是可能返回此代码，服务器处理请求时发生了冲突',
    RET.Gone:'客户端请求的资源已经不存在。410不同于404，如果资源以前有现在被永久删除了可使用410代码，网站设计人员可通过301代码指定资源的新位置',
    RET.LengthRequired:'服务器无法处理客户端发送的不带Content-Length的请求信息',
    RET.PreconditionFailed:'客户端请求信息的先决条件错误',
    RET.RequestEntityTooLarge:'由于请求的实体过大，服务器无法处理，因此拒绝请求。为防止客户端的连续请求，服务器可能会关闭连接。如果只是服务器暂时无法处理，则会包含一个Retry-After的响应信息',
    RET.RequestURITooLarge:'请求的URI过长（URI通常为网址），服务器无法处理',
    RET.UnsupportedMediaType:'服务器无法处理请求附带的媒体格式',
    RET.RequestedRangeNotSatisfiable:'客户端请求的范围无效',
    RET.ExpectationFailed:'服务器无法满足Expect的请求头信息',
    RET.InternalServerError:'服务器内部错误，无法完成请求',
    RET.NoImplemented:'服务器不支持请求的功能，无法完成请求',
    RET.BadGateway:'充当网关或代理的服务器，从远端服务器接收到了一个无效的请求',
    RET.ServiceUnavailable:'由于超载或系统维护，服务器暂时的无法处理客户端的请求。延时的长度可包含在服务器的Retry-After头信息中',
    RET.GatewayTimeout:'充当网关或代理的服务器，未及时从远端服务器获取请求',
    RET.HTTPVersionNotSupported:'服务器不支持请求的HTTP协议的版本，无法完成处理 ',	
}
		
	
		
		
		
		
	

    