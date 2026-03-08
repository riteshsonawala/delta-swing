package com.deltaswing.presentation.navigation

object NavRoutes {
    const val AUTH = "auth"
    const val PORTFOLIO = "portfolio"
    const val ADD_STOCK = "add_stock"
    const val EDIT_STOCK = "edit_stock/{stockId}"
    const val STOCK_DETAIL = "stock_detail/{stockId}"

    fun editStock(stockId: String) = "edit_stock/$stockId"
    fun stockDetail(stockId: String) = "stock_detail/$stockId"
}
