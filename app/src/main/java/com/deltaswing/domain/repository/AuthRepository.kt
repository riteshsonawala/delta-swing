package com.deltaswing.domain.repository

import com.google.firebase.auth.FirebaseUser
import kotlinx.coroutines.flow.Flow

interface AuthRepository {
    val currentUser: FirebaseUser?
    val isSignedIn: Boolean
    fun observeAuthState(): Flow<FirebaseUser?>
    suspend fun signInWithGoogle(idToken: String): FirebaseUser?
    suspend fun signOut()
}
