# Common Error Codes

| Code | Meaning |
|------|---------|
| 400 Bad Request | 请求参数格式错误、缺少必填字段或上下文超长 |
| 401 Unauthorized | API Key 错误、过期或未正确配置 |
| 402 Payment Required | 账户余额或 Plan 配额不足 |
| 403 Forbidden | API Key 无权限访问请求的模型或资源 |
| 404 Not Found | API 地址、路径或模型名错误 |
| 405 Method Not Allowed | HTTP 方法错误（如需要 POST 却用了 GET） |
| 408 Request Timeout | 请求超时（网络不稳或任务耗时过长） |
| 409 Conflict | 重复提交相同任务 |
| 413 Payload Too Large | 请求体过大（上下文或 base64 图片太长） |
| 415 Unsupported Media Type | 上传文件格式或 Content-Type 不支持 |
| 422 Unprocessable Entity | 参数值不合法（seed/分辨率/FPS 超范围） |
| 429 Too Many Requests | 请求频率超过 RPM 限制（免费用户约 20 RPM） |
| 431 Request Header Fields Too Large | 请求 Header 过大 |
| 499 Client Closed Request | 客户端提前断开连接 |
| 500 Internal Server Error | 服务器内部错误（参数触发异常或上游服务异常） |
| 502 Bad Gateway | 网关/代理无法连接上游服务（网络或 DNS 问题） |
| 503 Service Unavailable | 服务暂不可用（模型名错误、路由未启用或过载） |
| 504 Gateway Timeout | 上游服务响应超时（长任务或高峰期） |
| 520 Unknown Error | 未知错误（网络/网关/代理问题） |
| 522 Connection Timed Out | 网关连接上游超时 |
| 524 Timeout Occurred | 连接已建立但上游处理超时 |
