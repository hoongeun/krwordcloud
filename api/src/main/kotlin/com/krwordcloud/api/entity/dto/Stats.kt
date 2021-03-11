package com.krwordcloud.api.entity.dto

import lombok.Data
import java.util.*


//@Document
//@Data
//@AllArgsConstructor
//@NoArgsConstructor
//@EqualsAndHashCode
//data class Stats(val date: Date, val dataSize: UInt, val minDate: Date, val maxDate: Date): BasicEntity {
//}

@Data
data class Stats(
    val size: Long,
    val start: String,
    val end: String,
    val graph_size: Long,
    val rank_size: Long,
    val categories: List<String> = ArrayList(),
    val presses: List<String> = ArrayList()
)