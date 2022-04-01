package com.example.backend.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

import java.sql.Timestamp;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;
import java.util.Map;
import java.util.TimeZone;

@RestController
@RequestMapping("/sensor")
public class SensorController {

    @Autowired
    private JdbcTemplate jdbcTemplate;

    @Transactional
    @RequestMapping("/display")
    public List display() {
        String displaySQL = "select * from sensor;";
        List<Map<String, Object>> maps = jdbcTemplate.queryForList(displaySQL);
        return maps;
    }

    @Transactional
    @RequestMapping(value = "/add", method = RequestMethod.POST)
    public int add(@RequestBody Map params) {
        int sensor_id = (Integer) params.get("sensor_id");
        String existSensorIdSQL = "select * from sensor where sensor_id = ?;";
        boolean existSensorId = jdbcTemplate.queryForList(existSensorIdSQL, sensor_id).size() > 0;
        if (existSensorId) {
            return -1;
        }
        double x = (Double) params.get("x");
        double y = (Double) params.get("y");
        String existSensorLocSQL = "select * from sensor where x =? and y = ?;";
        boolean existSensorLoc = jdbcTemplate.queryForList(existSensorLocSQL, x, y).size() > 0;
        if (existSensorLoc) {
            return -2;
        }
        Timestamp last_charged = Timestamp.valueOf((String) params.get("last_charged"));
        String maintainer = (String) params.get("maintainer");
        if (maintainer.length() > 0) {
            String existWorkerSQL = "select * from worker where ssn=?;";
            boolean existWorker = jdbcTemplate.queryForList(existWorkerSQL, maintainer).size() > 0;
            if (!existWorker) {
                return -3;
            }
        }
        Timestamp last_read = Timestamp.valueOf((String) params.get("last_read"));
        double energy = (Double) params.get("energy");
        String insertSensorSQL;
        if (maintainer.length() == 0) {
            insertSensorSQL = "insert into sensor (sensor_id, x, y, last_charged,"
                    + "last_read, energy) values (?, ?, ?, ?, ?, ?)";
            int sensorRowChanged = jdbcTemplate.update(insertSensorSQL, sensor_id, x, y, last_charged, last_read, energy);
            if (sensorRowChanged > 0) {
                return 1;
            }
        } else {
            insertSensorSQL = "insert into sensor (sensor_id, x, y, last_charged, maintainer,"
                    + "last_read, energy) values (?, ?, ?, ?, ?, ?, ?)";
            int sensorRowChanged = jdbcTemplate.update(insertSensorSQL, sensor_id, x, y, last_charged, maintainer, last_read, energy);
            if (sensorRowChanged > 0) {
                return 1;
            }
        }
        return -4;
    }

    @Transactional
    @RequestMapping(value = "/update", method = RequestMethod.POST)
    public int update(@RequestBody Map params) {
        double x = (Double) params.get("x");
        double y = (Double) params.get("y");
        String existSensorLocSQL = "select * from sensor where x = ? and y = ?;";
        List<Map<String, Object>> existSensorResult = jdbcTemplate.queryForList(existSensorLocSQL, x, y);
        if (!(existSensorResult.size() > 0)) {
            return -1;
        }
        int sensor_id = (Integer) existSensorResult.get(0).get("sensor_id");
        double energy = (Double) params.get("energy");
        Timestamp last_charged = Timestamp.valueOf((String) params.get("last_charged"));
        SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        format.setTimeZone(TimeZone.getTimeZone("America/New_York"));
        String strReadDate = format.format(new Date());
        Timestamp last_read = Timestamp.valueOf(strReadDate);
        double temperature = (Double) params.get("temperature");
        String updateSensorSQL = "update sensor set last_charged=?, last_read=?,energy=? where x=? and y=?";
        int sensorRowChanged = jdbcTemplate.update(updateSensorSQL, last_charged, last_read, energy, x, y);
        if (sensorRowChanged <= 0) {
            return -2;
        }
        String insertReportSQL = "insert into report(sensor_id, report_time, temperature)" +
                "values (?, ?, ?)";
        int reportRowChanged = jdbcTemplate.update(insertReportSQL, sensor_id, last_read, temperature);
        if (reportRowChanged <= 0) {
            return -3;
        } else {
            if (temperature > 100) {
                return 2;
            }
            return 1;
        }
    }

    @Transactional
    @RequestMapping(value = "/ranking", method = RequestMethod.POST)
    public List rank(@RequestBody Map params) {
        int k = (Integer) params.get("k");
        String rankSQL = "select sensor_id, count(1) as report_cnt from report group by sensor_id order by report_cnt desc limit ?;";
        List<Map<String, Object>> maps = jdbcTemplate.queryForList(rankSQL, k);
        return maps;
    }
}
