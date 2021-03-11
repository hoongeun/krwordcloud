package com.krwordcloud.api.service

import com.krwordcloud.api.entity.dto.MergedTrend
import com.krwordcloud.api.entity.dto.Stats
import com.krwordcloud.api.entity.dto.TrendQuery

public interface TrendService {
    fun findByRange(trendQuery: TrendQuery): MergedTrend
    fun findStats(): Stats
}
