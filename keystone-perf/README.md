# fernet_uuid_compare

bin/ ---  程序目录  
data/ --- 用户名 token json 存放目录  
release/ ---  测试结果目录  

##bin/ 目录
auth.json ---- 模版  
benchmark ---- 测试文件   

perf-create-users.sh  ---- 生成测试用户（默认100）  
perf-delete-users.sh  ---- 删除测试用户（默认100）  
curl_user.sh  ----  多个测试用户json信息获取  
check_token_user.py ---- 多个测试用户token信息获取  

因token可多次使用 为减少其他是操作干扰使用  
latest_curl_user.sh ---- 单个测试用户json信息获取  
check_token_user_ben.py --- 单个测试用户token信息获取  

##data/目录
username json token   中间信息存放  
user_token_ben.json  
user_token_ben.txt
##release/ 目录 测试结果目录
latest_create_token ---- 单并发创建200次  
latest_create_token_concurrent  ----100并发创建2000次  
latest_validate_token ---- 单并发验证10000次  
latest_validate_token_concurrent ----100并发验证100000次

