package cn.ac.ucas.webgis.server.service;

import cn.ac.ucas.webgis.server.entity.Employee;
import cn.ac.ucas.webgis.server.mapper.EmployMapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import org.springframework.stereotype.Service;

@Service
public class EmployeeServiceImpl extends ServiceImpl<EmployMapper, Employee> implements EmployService{

}