---
aliases: "WebGis 课程作业, 'WebGis 课程作业'"
tags: 
cssclass:
source:
created: "2023-05-29 16:31"
updated: "2023-05-29 17:23"
---
# WebGis 课程作业

Welcome to the WebGIS Project! This project is a web-based Geographic Information System (GIS) application built using Vue.js, Cesium, and Java Spring Boot. It allows users to perform various GIS operations and visualize geographical data.

## 功能特性

- 特性1:
- 特性2:

## 安装与运行

以下是在本地环境中安装和运行该项目的步骤：

1. 克隆项目代码到本地机器：

```bash
git clone https://github.com/yottahub/WebGIS_Project.git
```

### 项目结构

```bash
. 
├── pom.xml 
├── src 
│ ├── lib # local libraries
│ ├── main 
│   ├── java 
│   │ └── cn.ac.ucas.webgis.server
│   │      ├── WebGisProjectApplication.java
│   │      ├── common 
│   │      │ └── Result.java 
│   │      ├── config 
│   │      │ └── WebMvcConfig.java 
│   │      ├── controller 
│   │      │ └── WebFeatureController.java 
│   │      ├── entity 
│   │      │ ├── # 项目使用实例
│   │      ├── mapper 
│   │      └── service
│   └── resources
│   ├── python # Python脚本
│   ├── static # 网页资源
│    └── page
│         ├── scripts 
│         └── styles
└── target
```

1. Frontend Setup: 
- Navigate to the `frontend` directory. 
- Install the dependencies using `npm`: 

```bash
npm install
```

1. Backend Setup: 
- Open the project in your Java IDE. 
- Configure the MySQL database connection in the `application.properties` file. 

1. Database Setup: 
- Create a new MySQL database named `webgis`. 
- Import the sample data provided in the `database` folder. 

1. Running the Application: 

- Frontend: In the `frontend` directory, run the following command: 

```bash 
npm run serve 
``` 

- Backend: Run the Java Spring Boot application from your IDE.

1. Open your web browser and access the application at [http://localhost:12345](http://localhost:12345).

 ## 技术栈

该项目使用以下技术和工具：

- 后端框架：Spring Boot
- 数据库：MySQL
- 前端框架：Vue-Cesium
- 版本控制：Git
- 构建工具：Maven

## License 

This project is licensed under the [MIT License](LICENSE)

## Acknowledgments 

- The project utilizes various open-source libraries and frameworks, including Vue.js, Cesium, MyBatis, and Spring Boot. 
- Special thanks to the contributors and maintainers of these open-source projects for their valuable work.
