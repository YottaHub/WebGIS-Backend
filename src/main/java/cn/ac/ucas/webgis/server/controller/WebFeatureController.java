package cn.ac.ucas.webgis.server.controller;

import cn.ac.ucas.webgis.server.common.Result;
import cn.ac.ucas.webgis.server.entity.IntPair;
import cn.ac.ucas.webgis.server.entity.IntTuple;
import cn.ac.ucas.webgis.server.entity.StrPair;
import cn.ac.ucas.webgis.server.entity.User;
import cn.ac.ucas.webgis.server.service.EmployService;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.servlet.http.HttpServletRequest;
import lombok.extern.slf4j.Slf4j;
import org.python.util.PythonInterpreter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.io.*;
import java.util.ArrayList;
import java.util.List;

@Slf4j
@RestController
@RequestMapping("/")
public class WebFeatureController {

    /** The path of the python scripts. */
    private static final String PYTHON_SCRIPTS_PATH = "/src/main/python/";
    @Autowired
    private EmployService employService;

    @PostMapping("/login")
    public Result<Object> login(HttpServletRequest request, @RequestBody User user) throws IOException, InterruptedException {
        System.out.println("Processing login request");

        // Modify the user object
        user.setUsername("后端逻辑?? + " + user.getUsername());

        // Execute Python script
        String pythonScript = "javaPythonFile.py";
        String[] command = new String[]{"python", pythonScript, "1", "2"};
        Process process = Runtime.getRuntime().exec(command);
        InputStream ins = process.getInputStream();
        BufferedReader reader = new BufferedReader(new InputStreamReader(ins));
        String output = reader.readLine();
        process.waitFor();

        return Result.success(output);
    }

    /**
     * Sample method for login.
     * @return Result object containing the list of StrPair objects.
     * @throws JsonProcessingException if there is an error while processing JSON.
     */
    @RequestMapping("/login")
    public Result<Object> tableData() throws JsonProcessingException {
        StrPair pair3J = new StrPair();
        pair3J.setName("");
        pair3J.setValue("1048");

        StrPair pairYM = new StrPair();
        pairYM.setName("");
        pairYM.setValue("735");

        StrPair pairYD = new StrPair();
        pairYD.setName("");
        pairYD.setValue("580");

        StrPair pairCY = new StrPair();
        pairCY.setName("");
        pairCY.setValue("484");

        StrPair pairPR = new StrPair();
        pairPR.setName("");
        pairPR.setValue("300");

        List<StrPair> list = new ArrayList<>();
        list.add(pair3J);
        list.add(pairYM);
        list.add(pairYD);
        list.add(pairCY);
        list.add(pairPR);

        ObjectMapper mapper = new ObjectMapper();
        String json = mapper.writeValueAsString(list);
        return Result.success(list);
    }

    /**
     * Sample method for testParam.
     * @param data the IntPair object.
     * @return Result object containing the list of StrPair objects.
     * @throws IOException if an I/O error occurs.
     * @throws InterruptedException if the current thread is interrupted.
     */
    @PostMapping("/loginhh1")
    public Result<Object> testParam(@RequestBody IntPair data) throws IOException, InterruptedException {
        List<StrPair> result = resend2args(data, "test1.py");
        return Result.success(result);
    }
    @PostMapping("/testParam2")
    public Result<Object> testParam2(@RequestBody IntPair data) throws IOException, InterruptedException {
        List<StrPair> result = resend2args(data, "jini.py");
        return Result.success(result);
    }
    @PostMapping("/yuzhifa")
    public Object transportGeoJson(@RequestBody IntTuple data)throws IOException, InterruptedException{
        System.out.println("阈值法");
        List<StrPair> result = resend3args(data, "transportGeojson.py");
        return Result.success(result);
    }

    @PostMapping("/tongjifa")
    public Object transportGeoJson1(@RequestBody IntTuple data)throws IOException, InterruptedException{
        System.out.println("统计数据比较法");
        List<StrPair> result = resend3args(data, "transportGeojson.py");
        return Result.success(result);
    }

    @PostMapping("/morphological")
    public Object morph(@RequestBody IntTuple data)throws IOException, InterruptedException{
        System.out.println("形态特征分析");
        List<StrPair> result = resend3args(data, "morphological.py");
        return Result.success(result);
    }


    /**
     * Helper method to resend two arguments to a Python script.
     * @param intPair the IntPair object.
     * @param scriptName the name of the Python script.
     * @return the list of StrPair objects.
     * @throws IOException if an I/O error occurs.
     * @throws InterruptedException if the current thread is interrupted.
     */
    private List<StrPair> resend2args(IntPair intPair, String scriptName) throws IOException, InterruptedException {
        StringBuilder oss = new StringBuilder();
        int first = intPair.getFirst();
        int second = intPair.getSecond();

        List<StrPair> resultList = new ArrayList<>();
        try {
            System.out.println("start");
            String[] args = new String[] { "python", PYTHON_SCRIPTS_PATH + scriptName,
                                            String.valueOf(first), String.valueOf(second) };
            Process process = Runtime.getRuntime().exec(args);
            BufferedReader in = new BufferedReader(new InputStreamReader(
                process.getInputStream(),"GB2312"
            ));
            String line;
            while ((line = in.readLine()) != null){
                String[] iss = line.split(":");
                System.out.println(line);
                StrPair pair = new StrPair();
                pair.setName(iss[0]);
                pair.setValue(iss[1]);
                resultList.add(pair);
                oss.append(line);
            }

            in.close();
            process.waitFor();
            System.out.println("end");
        } catch (Exception e) {
            e.printStackTrace();
        }

        System.out.println("返回数据成功：" + oss);
        return resultList;
    }

    /**
     * Helper method to resend three arguments to a Python script.
     * @param tuple the IntTuple object.
     * @param scriptName the name of the Python script.
     * @return the list of StrPair objects.
     * @throws IOException if an I/O error occurs.
     * @throws InterruptedException if the current thread is interrupted.
     */
    public List<StrPair> resend3args(IntTuple tuple, String scriptName) throws IOException, InterruptedException {
        StringBuilder oss = new StringBuilder();
        int first = tuple.getFirst();
        int second = tuple.getSecond();
        int third = tuple.getThird();

        List<StrPair> resultList = new ArrayList<>();
        try{
            System.out.println("start");
            String[] args = new String[] { "python", PYTHON_SCRIPTS_PATH + scriptName,
                                            String.valueOf(first), String.valueOf(second), String.valueOf(third) };
            Process pr = Runtime.getRuntime().exec(args);
            BufferedReader in = new BufferedReader(new InputStreamReader(
                    pr.getInputStream(),"GB2312"
            ));
            String line;
            while ((line = in.readLine()) != null){
                String[] iss = line.split(":");
                StrPair pair = new StrPair();
                pair.setName(iss[0]);
                pair.setValue(iss[1]);
                resultList.add(pair);
                oss.append(line);
            }
            in.close();
            pr.waitFor();
            System.out.println("end");
        }
        catch (Exception e){
            e.printStackTrace();
        }
        System.out.println("返回数据成功：" + oss);
        return resultList;
    }
}
