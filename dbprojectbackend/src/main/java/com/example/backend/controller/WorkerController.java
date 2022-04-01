package com.example.backend.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping(value = "/worker")
public class WorkerController {

    @Autowired
    private JdbcTemplate jdbcTemplate;

    @Transactional
    @RequestMapping("/display")
    public List display() {
        String displaySQL = "select * from worker;";
        List<Map<String, Object>> maps = jdbcTemplate.queryForList(displaySQL);
        return maps;
    }

    @Transactional
    @RequestMapping(value = "/add", method = RequestMethod.POST)
    public int add(@RequestBody Map params) {
        String ssn = (String) params.get("ssn");
        String existWorkerSQL = "select * from worker where ssn=?;";
        boolean existWorker = jdbcTemplate.queryForList(existWorkerSQL, ssn).size() > 0;
        if (existWorker) {
            return -1;
        }
        String name = (String) params.get("name");
        int rank = (Integer) params.get("rank");
        String employing_state = (String) params.get("employing_state");
        String existStateSQL = "select * from state where lower(abbreviation)=?";
        boolean existState = jdbcTemplate.queryForList(existStateSQL, employing_state.toLowerCase()).size() > 0;
        if (!existState) {
            return -2;
        }
        String insertWorkerSQL = "insert into worker(ssn, name, rank, employing_state)" +
                "values (?, ?, ?, ?);";
        int workerRowChanged = jdbcTemplate.update(insertWorkerSQL, ssn, name, rank, employing_state.toUpperCase());
        if (workerRowChanged > 0) {
            return 1;
        }
        return -3;
    }

    @Transactional
    @RequestMapping(value = "/switch", method = RequestMethod.POST)
    public int switchDuty(@RequestBody Map params) {
        String worker1 = (String) params.get("name1");
        String worker2 = (String) params.get("name2");
        boolean cond1 = worker1.equals(worker2);
        if (cond1) {
            return -1;
        }
        String workerExistSQL = "select * from worker where name=?;";
        List<Map<String, Object>> worker1Result = jdbcTemplate.queryForList(workerExistSQL, worker1);
        List<Map<String, Object>> worker2Result = jdbcTemplate.queryForList(workerExistSQL, worker2);
        boolean existWorker1 = worker1Result.size() > 0;
        boolean existWorker2 = worker2Result.size() > 0;
        if ((!existWorker1) && existWorker2) {
            return -2;
        }
        if (existWorker1 && (!existWorker2)) {
            return -3;
        }
        if ((!existWorker1) && (!existWorker2)) {
            return -4;
        }
        String ssn1 = (String) worker1Result.get(0).get("ssn");
        String ssn2 = (String) worker2Result.get(0).get("ssn");
        String employing_state1 = (String) worker1Result.get(0).get("employing_state");
        String employing_state2 = (String) worker2Result.get(0).get("employing_state");
        if (!employing_state1.equals(employing_state2)) {
            return -5;
        }
        String switchSQL = "update sensor set maintainer = (case when maintainer = ? then ? " +
                "when maintainer = ? then ? else maintainer end);";
        int workerRowChanged = jdbcTemplate.update(switchSQL, ssn1, ssn2, ssn2, ssn1);
        if (workerRowChanged > 0) {
            return 1;
        }
        return -6;
    }

    @Transactional
    @RequestMapping(value = "/topk", method = RequestMethod.POST)
    public List topK(@RequestBody Map params) {
        int k = (Integer) params.get("k");
        String queryWorkerSQL = "select name, count(1) as sensor_cnt from worker, sensor " +
                "where worker.ssn = sensor.maintainer and sensor.energy <= 2 group by name " +
                "order by sensor_cnt desc limit ?;";
        List<Map<String, Object>> maps = jdbcTemplate.queryForList(queryWorkerSQL, k);
        return maps;
    }

}
