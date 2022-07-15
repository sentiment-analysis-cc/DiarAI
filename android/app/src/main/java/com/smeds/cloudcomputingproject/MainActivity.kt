package com.smeds.cloudcomputingproject

import android.content.Intent
import android.content.SharedPreferences
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.preference.PreferenceManager
import android.util.Log
import android.view.View
import android.widget.EditText
import android.widget.Toast
import androidx.lifecycle.lifecycleScope
import com.liftric.cognito.idp.IdentityProviderClient
import kotlinx.coroutines.launch



class MainActivity : AppCompatActivity() {

    lateinit var mail : String
    lateinit var password : String
    lateinit var prefs : SharedPreferences
    val provider = IdentityProviderClient("us-east-1", "2iujemsjc32fgm5vj2sb5b7s77")

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        prefs = PreferenceManager.getDefaultSharedPreferences(this)

    }

    fun signIn(view: View) {

        mail = findViewById<EditText>(R.id.email_text).text.toString()
        password = findViewById<EditText>(R.id.pw_text).text.toString()

        lifecycleScope.launch {

            lateinit var accessToken : String
            var res = false
            provider.signIn(mail, password).fold(
                onSuccess = {
                    accessToken = it.AuthenticationResult?.AccessToken!!
                    res = true
                },
                onFailure = {
                    Toast.makeText(this@MainActivity, "Signin fail ${it.message}", Toast.LENGTH_SHORT).show()
                    Log.i("LOGIN", "${it.message}")
                    res = false
                }
            )
            if (!res) return@launch
            lateinit var usernameString : String
            provider.getUser(accessToken).fold(
                onSuccess = {
                    Toast.makeText(this@MainActivity,"Username: ${it.Username}",Toast.LENGTH_SHORT).show()
                    usernameString = it.Username
                    res = true
                },
                onFailure = {
                    Log.i("LOGIN", "${it.message}")
                    res = false
                }
            )
            if (!res) return@launch

            val prefsEditor = prefs.edit()
            prefsEditor.putString("username", usernameString)
            prefsEditor.putString("token", accessToken)
            prefsEditor.putBoolean("loggedIn", true)
            prefsEditor.commit()

            val intent = Intent(this@MainActivity, DiaryEntryActivity::class.java)
            startActivity(intent)
        }
    }
}