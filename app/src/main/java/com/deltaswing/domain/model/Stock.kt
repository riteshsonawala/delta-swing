package com.deltaswing.domain.model

data class Stock(
    val id: String = "",
    val userId: String = "",
    val symbol: String = "",
    val basePrice: Double = 0.0,
    val deltaPercentage: Double = 5.0,
    val currentPrice: Double? = null,
    val lastUpdated: Long = 0L
) {
    val thresholdPrice: Double
        get() = basePrice * (1 - deltaPercentage / 100)

    val isBelowThreshold: Boolean
        get() = currentPrice != null && currentPrice <= thresholdPrice

    val priceChangePercent: Double?
        get() = currentPrice?.let { ((it - basePrice) / basePrice) * 100 }
}
