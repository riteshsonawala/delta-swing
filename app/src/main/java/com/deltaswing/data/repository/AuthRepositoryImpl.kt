package com.deltaswing.data.repository

import com.deltaswing.domain.repository.AuthRepository
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.auth.FirebaseUser
import com.google.firebase.auth.GoogleAuthProvider
import kotlinx.coroutines.channels.awaitClose
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.callbackFlow
import kotlinx.coroutines.tasks.await
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class AuthRepositoryImpl @Inject constructor(
    private val firebaseAuth: FirebaseAuth
) : AuthRepository {

    override val currentUser: FirebaseUser?
        get() = firebaseAuth.currentUser

    override val isSignedIn: Boolean
        get() = firebaseAuth.currentUser != null

    override fun observeAuthState(): Flow<FirebaseUser?> = callbackFlow {
        val listener = FirebaseAuth.AuthStateListener { auth ->
            trySend(auth.currentUser)
        }
        firebaseAuth.addAuthStateListener(listener)
        awaitClose { firebaseAuth.removeAuthStateListener(listener) }
    }

    override suspend fun signInWithGoogle(idToken: String): FirebaseUser? {
        val credential = GoogleAuthProvider.getCredential(idToken, null)
        val result = firebaseAuth.signInWithCredential(credential).await()
        return result.user
    }

    override suspend fun signOut() {
        firebaseAuth.signOut()
    }
}
