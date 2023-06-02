package cn.ac.ucas.webgis.server.controller;

import cn.ac.ucas.webgis.server.common.IntPair;
import cn.ac.ucas.webgis.server.common.IntTuple;
import cn.ac.ucas.webgis.server.common.Result;
import cn.ac.ucas.webgis.server.common.StrPair;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.sql.SQLOutput;
import java.time.LocalTime;
import java.util.ArrayList;
import java.util.List;

@Slf4j
@RestController
@RequestMapping("/")
public class WebFeatureController {

    /** The path of the python scripts. */
    private static final String PYTHON_SCRIPTS_PATH = System.getProperty("user.dir") + File.separator + "src" +
                                                      File.separator + "main" + File.separator + "python" +
                                                      File.separator + "scripts" + File.separator;
    /** The python command. */
    private static final String PYTHON = "python3";

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
    @PostMapping("/yuzhifa")
    public Object transportGeoJson(@RequestBody IntTuple data)throws IOException, InterruptedException{
        System.out.println("阈值法");
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
        int first = intPair.getSelectedCityIndex();
        int second = intPair.getSelectedYearIndex();

        System.out.println("当前时间: " + LocalTime.now() + "参数1：" + first + "参数2：" + second + "脚本名：" +
                            PYTHON + " " + PYTHON_SCRIPTS_PATH + scriptName);
        List<StrPair> resultList = new ArrayList<>();
        try {
            System.out.println("start");
            String[] args = new String[] { PYTHON, PYTHON_SCRIPTS_PATH + scriptName,
                                            String.valueOf(first), String.valueOf(second) };
            System.out.println();
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
        int first = tuple.getSelectedCityIndex();
        int second = tuple.getSelectedYearIndex();
        int third = tuple.getSplitValue();

        System.out.println("当前时间: " + LocalTime.now() + "\n参数1：" + first + "\t参数2：" + second + "\t参数3：" + third +
                           "\n脚本名：" + PYTHON + " " + PYTHON_SCRIPTS_PATH + scriptName);
        List<StrPair> resultList = new ArrayList<>();
        try{
            System.out.println("start");
            String[] args = new String[] { PYTHON, PYTHON_SCRIPTS_PATH + scriptName,
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
