package cn.ac.ucas.webgis.server.entity;

import lombok.Data;

@Data
public class User {
    private String username;
    private String password;
    private int code;
    private boolean checked;
}
