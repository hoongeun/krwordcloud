package com.krwordcloud.api.entity.dto

import lombok.Data

@Data
data class MergedTrend(val start: String, val end: String, var size: Long, val score: MutableMap<String, Double>)
