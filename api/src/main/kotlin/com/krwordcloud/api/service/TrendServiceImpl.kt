package com.krwordcloud.api.service

import com.krwordcloud.api.entity.Stats
import com.krwordcloud.api.entity.Trend
import com.krwordcloud.api.entity.dto.MergedTrend
import com.krwordcloud.api.entity.dto.TrendQuery
import com.krwordcloud.api.repository.StatsRepository
import com.krwordcloud.api.repository.TrendRepository
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
        val stats = findLatestStats()

        if (trendQuery.start != null
            && ((DateUtil.parseDate(trendQuery.start) == null
            || (DateUtil.parseDate(trendQuery.start)?.before(DateUtil.parseDate(stats.start)) == true)))
        ) {
            throw BadRequestException("invalid params - start >= ${stats.start}")
        }

        if (trendQuery.end != null
            && ((DateUtil.parseDate(trendQuery.end) == null
            || (DateUtil.parseDate(trendQuery.end)?.after(DateUtil.parseDate(stats.end)) == true)))
        ) {
            throw BadRequestException("invalid params - end <= ${stats.end}")
        }

        if (trendQuery.categories != null && !stats.categories.containsAll(trendQuery.categories)) {
            throw BadRequestException("invalid params - categories")
        }

        if (trendQuery.presses != null && !stats.presses.containsAll(trendQuery.presses)) {
            throw BadRequestException("invalid params - presses")
        }

        val result = MergedTrend(trendQuery.start ?: stats.start,
            trendQuery.end ?: stats.end, 0, mutableMapOf<String, Double>())

        val trends = trendRepository.findByRange(
            trendQuery.start ?: stats.start,
            trendQuery.end ?: stats.end,
            trendQuery.categories,
            trendQuery.presses)

        if (trends.isNotEmpty()) {
            result.start = trends.first().date
            result.end = trends.last().date
        }

        return trends.fold(result,
            { total: MergedTrend, next: Trend ->
                total.size += next.size
                for ((k, v) in next.score) {
                    total.score[k] = (total.score[k] ?: 0.0) + v
                }
                total
            })
    }

    override fun findLatestStats(): Stats {
        return statsRepository.findLatestStats()
    }

    override fun findAllStats(): List<Stats> {
        return statsRepository.findAll().toList()
    }
}
