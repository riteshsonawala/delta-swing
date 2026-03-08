package com.deltaswing.presentation.navigation

import androidx.compose.runtime.Composable
import androidx.navigation.NavHostController
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.navArgument
import com.deltaswing.presentation.addstock.AddEditStockScreen
import com.deltaswing.presentation.auth.AuthScreen
import com.deltaswing.presentation.portfolio.PortfolioScreen
import com.deltaswing.presentation.stockdetail.StockDetailScreen

@Composable
fun AppNavGraph(
    navController: NavHostController,
    startDestination: String
) {
    NavHost(
        navController = navController,
        startDestination = startDestination
    ) {
        composable(NavRoutes.AUTH) {
            AuthScreen(
                onSignInSuccess = {
                    navController.navigate(NavRoutes.PORTFOLIO) {
                        popUpTo(NavRoutes.AUTH) { inclusive = true }
                    }
                }
            )
        }

        composable(NavRoutes.PORTFOLIO) {
            PortfolioScreen(
                onAddStock = { navController.navigate(NavRoutes.ADD_STOCK) },
                onEditStock = { stockId -> navController.navigate(NavRoutes.editStock(stockId)) },
                onStockDetail = { stockId -> navController.navigate(NavRoutes.stockDetail(stockId)) },
                onSignOut = {
                    navController.navigate(NavRoutes.AUTH) {
                        popUpTo(NavRoutes.PORTFOLIO) { inclusive = true }
                    }
                }
            )
        }

        composable(NavRoutes.ADD_STOCK) {
            AddEditStockScreen(
                stockId = null,
                onNavigateBack = { navController.popBackStack() }
            )
        }

        composable(
            route = NavRoutes.EDIT_STOCK,
            arguments = listOf(navArgument("stockId") { type = NavType.StringType })
        ) { backStackEntry ->
            val stockId = backStackEntry.arguments?.getString("stockId")
            AddEditStockScreen(
                stockId = stockId,
                onNavigateBack = { navController.popBackStack() }
            )
        }

        composable(
            route = NavRoutes.STOCK_DETAIL,
            arguments = listOf(navArgument("stockId") { type = NavType.StringType })
        ) { backStackEntry ->
            val stockId = backStackEntry.arguments?.getString("stockId") ?: return@composable
            StockDetailScreen(
                stockId = stockId,
                onNavigateBack = { navController.popBackStack() },
                onEditStock = { navController.navigate(NavRoutes.editStock(stockId)) }
            )
        }
    }
}
