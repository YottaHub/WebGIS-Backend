package cn.ac.ucas.webgis.server.common;

import lombok.Data;

import java.util.HashMap;
import java.util.Map;

@Data
public class Result<T> {
    private int errorCode;
    private String errorMsg;
    private T data;
    private Map<String, Object> map = new HashMap<>();

    public Result() {
        this.errorCode = 0;
        this.errorMsg = "success";
    }

    public static <T> Result<T> success(T data) {
        Result<T> result = new Result<>();
        result.setErrorCode(1);
        result.setData(data);
        return result;
    }

    public static <T> Result<T> error(String msg) {
        Result<T> result = new Result<>();
        result.setErrorCode(0);
        result.setErrorMsg(msg);
        return result;
    }

    public Result<T> add(String key, Object value) {
        this.map.put(key, value);
        return this;
    }
}
