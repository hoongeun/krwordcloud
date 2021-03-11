package com.krwordcloud.api.service

import com.krwordcloud.api.entity.Trend
import com.krwordcloud.api.entity.dto.MergedTrend
import com.krwordcloud.api.entity.dto.Stats
import com.krwordcloud.api.entity.dto.TrendQuery
import com.krwordcloud.api.repositories.StatsRepository
import com.krwordcloud.api.repositories.TrendRepository
import com.krwordcloud.api.utils.BadRequestException
import com.krwordcloud.api.utils.DateUtil
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.stereotype.Service

@Service
class TrendServiceImpl(
    @Autowired private val trendRepository: TrendRepository,
    @Autowired private val statsRepository: StatsRepository,
) : TrendService {
    override fun findByRange(trendQuery: TrendQuery): MergedTrend {
        val stats = findStats()
        if (trendQuery.start != null
            && (DateUtil.parseDate(trendQuery.start) == null
            || (DateUtil.parseDate(trendQuery.start)?.before(DateUtil.parseDate(stats.start)) == true))
        ) {
            throw BadRequestException("invalid params - start >= ${stats.start}")
        }
        if (trendQuery.end != null
            && (DateUtil.parseDate(trendQuery.end) == null
            || (DateUtil.parseDate(trendQuery.end)?.after(DateUtil.parseDate(stats.end)) == true))
        ) {
            throw BadRequestException("invalid params - end <= ${stats.end}")
        }
        if (trendQuery.categories != null && !stats.categories.containsAll(trendQuery.categories)) {
            throw BadRequestException("invalid params - categories")
        }
        if (trendQuery.presses != null && !stats.presses.containsAll(trendQuery.presses)) {
            throw BadRequestException("invalid params - presses")
        }
        val trends = trendRepository.findByRange(trendQuery.start ?: stats.start,
            trendQuery.end ?: stats.end,
            trendQuery.categories,
            trendQuery.presses)
        return trends.fold(MergedTrend(trends.first().date, trends.last().date, 0, mutableMapOf<String, Double>()),
            { total: MergedTrend, next: Trend ->
                total.size += next.size
                for ((k, v) in next.score) {
                    total.score.put(k, (total.score[k] ?: 0.0) + (v * next.graph_size))
                }
                return total
            })
    }

    override fun findStats(): Stats {
        return statsRepository.findStats()
    }
}
