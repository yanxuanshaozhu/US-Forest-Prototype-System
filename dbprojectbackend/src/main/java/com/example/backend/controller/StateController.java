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
@RequestMapping(value = "/state")
public class StateController {
    @Autowired
    private JdbcTemplate jdbcTemplate;

    @Transactional
    @RequestMapping("/display")
    public List display() {
        String displaySQL = "select * from state;";
        List<Map<String, Object>> maps = jdbcTemplate.queryForList(displaySQL);
        return maps;
    }

    @Transactional
    @RequestMapping(value = "/add", method = RequestMethod.POST)
    public int add(@RequestBody Map params) {
        String name = (String) params.get("name");
        String existStateSQL = "select * from state where name = ?;";
        boolean existState = jdbcTemplate.queryForList(existStateSQL, name).size() > 0;
        if (existState) {
            return -1;
        }
        String existAbbrSQL = "select * from state where abbreviation = ?;";
        String abbreviation = (String) params.get("abbreviation");
        boolean existAbbr = jdbcTemplate.queryForList(existAbbrSQL, abbreviation).size() > 0;
        if (existAbbr) {
            return -2;
        }
        double area = (Double) params.get("area");
        int population = (Integer) params.get("population");
        String insertStateSQL = "insert into state (name, abbreviation, area, population)"
                + " values(?, ?, ?, ?)";
        int stateRowChanged = jdbcTemplate.update(insertStateSQL, name, abbreviation, area, population);
        if (stateRowChanged > 0) {
            return 1;
        }
        return -2;

    }
}
