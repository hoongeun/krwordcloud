package com.krwordcloud.api.entity.dto

import lombok.Data

@Data
data class MergedTrend(var start: String, var end: String, var size: Long, val score: MutableMap<String, Double>)
