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
import okhttp3.*
import java.io.IOException
import java.lang.Exception

class DiaryEntryActivity : AppCompatActivity() {

    lateinit var title : String
    lateinit var entry : String
    lateinit var username : String
    lateinit var prefs : SharedPreferences
    val url = "blwdljp75pvc5eswhthjx66a4m0hdbyv.lambda-url.us-east-1.on.aws"


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_diary_entry)

        prefs = PreferenceManager.getDefaultSharedPreferences(this)
    }

    fun getEntries(view:View) {
        val intent = Intent(this, GetEntriesActivity::class.java)
        startActivity(intent)
    }

    fun submitEntry(view: View) {

        title = findViewById<EditText>(R.id.text_title).text.toString()
        entry = findViewById<EditText>(R.id.text_entry).text.toString()
        username = prefs.getString("username", "").toString()

        val client = OkHttpClient()

        val httpUrl = HttpUrl.Builder()
            .scheme("https")
            .host(url)
            .addQueryParameter("username", username)
            .addQueryParameter("diaryTitle", title)
            .addQueryParameter("text", entry)
            .build()

        Log.i("ENTRY", httpUrl.toString())

        val request = Request.Builder()
            .url(httpUrl)
            .build()

        try {
            client.newCall(request).enqueue(object : Callback {
                override fun onFailure(call: Call, e: IOException) {
                    e.printStackTrace()
                }

                override fun onResponse(call: Call, response: Response) {
                    response.use {
                        if (!response.isSuccessful) throw IOException("Unexpected code $response")

                        for ((name, value) in response.headers) {
                            println("$name: $value")
                        }

                        println(response.body!!.string())
                    }
                }
            })
        } catch (e : Exception) {
            Log.i("ENTRY", e.message!!)
            return
        }

    }
}