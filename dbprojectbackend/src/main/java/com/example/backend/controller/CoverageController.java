package com.example.backend.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/coverage")
public class CoverageController {

    @Autowired
    private JdbcTemplate jdbcTemplate;

    @Transactional
    @RequestMapping("/display")
    public List display() {
        String displaySQL = "select * from coverage;";
        List<Map<String, Object>> maps = jdbcTemplate.queryForList(displaySQL);
        return maps;
    }
}
