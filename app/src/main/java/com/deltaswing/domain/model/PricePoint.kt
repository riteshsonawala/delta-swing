package com.deltaswing.domain.model

data class PricePoint(
    val date: String,
    val open: Double,
    val high: Double,
    val low: Double,
    val close: Double,
    val volume: Long
)
