package com.krwordcloud.api.controller

import com.krwordcloud.api.entity.dto.MergedTrend
import com.krwordcloud.api.entity.dto.Stats
import com.krwordcloud.api.entity.dto.TrendQuery
import com.krwordcloud.api.service.TrendService
import org.springframework.http.MediaType.APPLICATION_JSON_VALUE
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RequestMethod.GET
import org.springframework.web.bind.annotation.RequestParam
import org.springframework.web.bind.annotation.RestController

@RestController
@RequestMapping("/v1/trend")
class TrendController(private val trendService: TrendService) {
    @RequestMapping(value = [""], method = [GET], produces = [APPLICATION_JSON_VALUE])
    fun findByRange(@RequestParam(required = false) start: String?, @RequestParam(required = false) end: String?, @RequestParam(required = false, value="category") categories: String?, @RequestParam(required = false, value="press") presses: String?): MergedTrend {
        val trendQuery = TrendQuery(start, end, categories?.split(","), presses?.split(","))
        return trendService.findByRange(trendQuery)
    }

    @RequestMapping(value = ["/stats"], method = [GET], produces = [APPLICATION_JSON_VALUE])
    fun findStats(): Stats {
        return trendService.findStats()
    }
}
