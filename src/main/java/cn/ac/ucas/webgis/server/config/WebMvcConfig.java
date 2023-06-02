package cn.ac.ucas.webgis.server.config;

import lombok.extern.slf4j.Slf4j;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.EnableWebMvc;
import org.springframework.web.servlet.config.annotation.ResourceHandlerRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurationSupport;

@Slf4j
@Configuration
@EnableWebMvc
public class WebMvcConfig extends WebMvcConfigurationSupport {

    @Override
    protected void addResourceHandlers(ResourceHandlerRegistry registry) {
        log.info("开始静态资源映射");
        registry
                .addResourceHandler("/backend/**")
                .addResourceLocations("classpath:/backend/")
                .setCachePeriod(3600) // Set cache control to 1 hour (in seconds)
                .resourceChain(true);

        registry
                .addResourceHandler("/front/**")
                .addResourceLocations("classpath:/front/")
                .setCachePeriod(3600) // Set cache control to 1 hour (in seconds)
                .resourceChain(true);
    }

}
