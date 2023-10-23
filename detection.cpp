#include<curl/curl.h>
#include<chrono>
#include<thread>
#include<cstdlib>
#include<iostream>
#include<string>
#include <vector>
#include <cstring>
#include <cstdio>

const std::string s = "python main.py";
const std::string url = "https://sctapi.ftqq.com/SCT67690TLrXfrH1z0SKmUdxwJoeQmgQ5.send?";
std::string data = "title=自动报名已停止运行&desp=自动报名已停止运行";

bool jiance(){
	FILE* fi = popen("ps -ef", "r");
	if(!fi){
		return false;
	}

	std::vector<std::string> output;
	char buffer[128];
	while(fgets(buffer, sizeof(buffer), fi) != nullptr){
		output.push_back(buffer);
	}

	pclose(fi);

	for(const std::string& i : output){
		if(i.find(s) != std::string::npos){
			return true;
		}
	}
	return false;
}

// 回调函数，用于处理响应数据
size_t WriteCallback(void* contents, size_t size, size_t nmemb, std::string* output) {
    size_t totalSize = size * nmemb;
    output->append(static_cast<char*>(contents), totalSize);
    return totalSize;
}

int main(){
    // 初始化libcurl
    CURL* curl;
    CURLcode res;

    curl = curl_easy_init();
	
	while(true){
		if(!jiance()){

		    if (curl) {
		        // 设置POST请求选项
		        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
		        if(system("nohup python main.py&") == 0){
		        	
		        	if(jiance()){
		        		data += "\n重启脚本成功";
		        	}
		        	else{
		        		data += "\n 重启脚本失败";
		        	}
		        }
		        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, data.c_str());
		
		        // 设置回调函数来处理响应数据
		        std::string response;
		        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
		        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response);
		
		        // 执行POST请求
		        res = curl_easy_perform(curl);
		        if (res == CURLE_OK) {
		            std::cout << "发送成功" << std::endl;
		        }
		    }
		
			curl_easy_cleanup(curl);	
		}
		
		std::this_thread::sleep_for(std::chrono::seconds(60));
	}
	return 0;
}
