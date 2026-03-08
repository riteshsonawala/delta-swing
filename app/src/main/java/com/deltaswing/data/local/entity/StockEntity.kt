package com.deltaswing.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey
import com.deltaswing.domain.model.Stock

@Entity(tableName = "stocks")
data class StockEntity(
    @PrimaryKey
    val id: String,
    val userId: String,
    val symbol: String,
    val basePrice: Double,
    val deltaPercentage: Double,
    val currentPrice: Double?,
    val lastUpdated: Long
) {
    fun toDomain(): Stock = Stock(
        id = id,
        userId = userId,
        symbol = symbol,
        basePrice = basePrice,
        deltaPercentage = deltaPercentage,
        currentPrice = currentPrice,
        lastUpdated = lastUpdated
    )

    companion object {
        fun fromDomain(stock: Stock): StockEntity = StockEntity(
            id = stock.id,
            userId = stock.userId,
            symbol = stock.symbol,
            basePrice = stock.basePrice,
            deltaPercentage = stock.deltaPercentage,
            currentPrice = stock.currentPrice,
            lastUpdated = stock.lastUpdated
        )
    }
}
