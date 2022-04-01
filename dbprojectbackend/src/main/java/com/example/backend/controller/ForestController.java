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
@RequestMapping("/forest")
public class ForestController {
    @Autowired
    private JdbcTemplate jdbcTemplate;

    @Transactional
    @RequestMapping("/display")
    public List display() {
        String displaySQL = "select * from forest;";
        List<Map<String, Object>> maps = jdbcTemplate.queryForList(displaySQL);
        return maps;
    }

    @Transactional
    @RequestMapping(value = "/add", method = RequestMethod.POST)
    public int add(@RequestBody Map params) {
        String name = (String) params.get("name");
        String existForestSQL = "select * from forest where name=?";
        boolean existForest = jdbcTemplate.queryForList(existForestSQL, name).size() > 0;
        if (existForest) {
            return -1;
        }
        String state = (String) params.get("state");
        String existStateSQL = "select * from state where lower(name)=?";
        List<Map<String, Object>> stateResult = jdbcTemplate.queryForList(existStateSQL, state.toLowerCase());
        if (!(stateResult.size() > 0)) {
            return -2;
        }
        String abbreviation = (String) stateResult.get(0).get("abbreviation");
        String sizeSQL = "select * from forest;";
        String forest_no = String.valueOf(jdbcTemplate.queryForList(sizeSQL).size() + 1);
        double area = (Double) params.get("area");
        double acid_level = (Double) params.get("acid_level");
        double mbr_xmin = (Double) params.get("mbr_xmin");
        double mbr_xmax = (Double) params.get("mbr_xmax");
        double mbr_ymin = (Double) params.get("mbr_ymin");
        double mbr_ymax = (Double) params.get("mbr_ymax");
        String insertForestSQL = "insert into forest (forest_no, name, area, acid_level, mbr_xmin, mbr_xmax,"
                + "mbr_ymin, mbr_ymax) values (?,?,?,?,?,?,?,?)";
        int forestRowChanged = jdbcTemplate.update(insertForestSQL, forest_no, name, area, acid_level, mbr_xmin, mbr_xmax, mbr_ymin, mbr_ymax);
        String insertCoverageSQL = "insert into coverage(forest_no, state, percentage, area)"
                + "values (?, ?, ?, ?)";
        int coverageRowChanged = jdbcTemplate.update(insertCoverageSQL, forest_no, abbreviation, 1, area);

        if (forestRowChanged > 0 && coverageRowChanged > 0) {
            return 1;
        } else {
            return -3;
        }
    }

    @Transactional
    @RequestMapping(value = "/update", method = RequestMethod.POST)
    public int update(@RequestBody Map params) {
        String name = (String) params.get("name");
        String existForestSQL = "select * from forest where name=?;";
        List<Map<String, Object>> existForestResult = jdbcTemplate.queryForList(existForestSQL, name);
        if (!(existForestResult.size() > 0)) {
            return -1;
        }
        String forest_no = (String) existForestResult.get(0).get("forest_no");
        double area = (Double) params.get("area");
        String updateForestSQL = "update forest set area =? where name =?;";
        int forestRowChanged = jdbcTemplate.update(updateForestSQL, area, name);
        String abbreviation = (String) params.get("state");
        String existStateSQL = "select * from state where lower(abbreviation)=?;";
        boolean existState = jdbcTemplate.queryForList(existStateSQL, abbreviation.toLowerCase()).size() > 0;
        if (!existState) {
            return -2;
        }
        String deleteCoverageSQL = "delete from coverage where forest_no=?";
        int coverageRowChanged1 = jdbcTemplate.update(deleteCoverageSQL, forest_no);
        String insertCoverageSQL = "insert into coverage (forest_no, state, percentage, area)" +
                "values (?, ?, ?, ?);";
        int coverageRowChanged2 = jdbcTemplate.update(insertCoverageSQL, forest_no, abbreviation, 1.0, area);
        if (forestRowChanged > 0 && coverageRowChanged1 > 0 && coverageRowChanged2 > 0) {
            return 1;
        }
        return -3;
    }
}
