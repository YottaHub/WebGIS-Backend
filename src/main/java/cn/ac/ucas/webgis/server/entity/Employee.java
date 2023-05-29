package cn.ac.ucas.webgis.server.entity;

import com.baomidou.mybatisplus.annotation.FieldFill;
import com.baomidou.mybatisplus.annotation.TableField;
import lombok.Data;

import java.io.Serial;
import java.io.Serializable;
import java.time.LocalDateTime;

@Data
public class Employee implements Serializable {
    @Serial
    private static final long serialVersionUID = 1L;
    private Long id;
    private String name;
    private String password;
    private String gender;
    private String username;
    private String idNumber;
    private String phone;
    private Integer status;
    private LocalDateTime createTime;
    private LocalDateTime updateTime;

    @TableField(fill = FieldFill.INSERT)
    private long createUser;

    @TableField(fill = FieldFill.INSERT_UPDATE)
    private long updateUser;
}