package com.krwordcloud.api.service

import com.krwordcloud.api.entity.Stats
import com.krwordcloud.api.entity.dto.MergedTrend
import com.krwordcloud.api.entity.dto.TrendQuery

interface TrendService {
    fun findByRange(trendQuery: TrendQuery): MergedTrend
    fun findLatestStats(): Stats
    fun findAllStats(): List<Stats>
}
