package cn.ac.ucas.webgis.server.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import cn.ac.ucas.webgis.server.entity.Employee;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface EmployMapper extends BaseMapper<Employee> {

}