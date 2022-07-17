package com.smeds.cloudcomputingproject

import android.app.Activity
import android.content.Context
import android.content.SharedPreferences
import android.preference.PreferenceManager
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.appcompat.app.AlertDialog
import androidx.recyclerview.widget.RecyclerView
import okhttp3.*
import org.json.JSONObject
import java.io.IOException


class EntryRecyclerAdapter (context: Context, entry : List<DiaryEntry>) :
    RecyclerView.Adapter<EntryRecyclerAdapter.DiaryEntryHolder>() {

    var context = context
    var entry = entry
    val url = "uuq3nqiwkutez37nremubegf6i0xqjsz.lambda-url.us-east-1.on.aws"
    lateinit var listener : EntryClickListener
    lateinit var dialog : AlertDialog
    lateinit var prefs : SharedPreferences

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): DiaryEntryHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.diary_list_items, parent, false)
        prefs = PreferenceManager.getDefaultSharedPreferences(context)
        return DiaryEntryHolder(view)
    }

    override fun onBindViewHolder(holder: DiaryEntryHolder, position: Int) {
        val title = entry[position].title
        val sentiment = entry[position].sentiment
        val date = entry[position].date
        val id = entry[position].id

        holder.txtDate.text = date
        holder.txtTitle.text = title
        holder.txtSentiment.text = sentiment.toString()
        holder.txtId = id

    }

    override fun getItemCount(): Int {
        return entry.count()
    }

    interface EntryClickListener {
        fun onItemClick(view : View, id : String)
    }

    inner class DiaryEntryHolder (itemView : View) : RecyclerView.ViewHolder(itemView), View.OnClickListener {
        val txtDate : TextView
        val txtTitle : TextView
        val txtSentiment : TextView
        lateinit var txtId : String
        lateinit var listener : EntryClickListener

        init {
            txtDate = itemView.findViewById(R.id.textView_date_data)
            txtTitle = itemView.findViewById(R.id.textView_title_data)
            txtSentiment = itemView.findViewById(R.id.textview_sentiment_data)
            itemView.setOnClickListener(this)
        }

        fun setDetails(entry : DiaryEntry) {
            //txtDate.text = entry.date
            txtTitle.text = entry.title
            txtSentiment.text = entry.sentiment.toString()
        }

        override fun onClick(v: View) {
            Log.i("DiaryEntryHolder", "Clicked on item ${txtTitle.text}")

            val client = OkHttpClient()

            val httpUrl = HttpUrl.Builder()
                .scheme("https")
                .host(url)
                //.addQueryParameter("username", username)
                .addQueryParameter("token", prefs.getString("token", "").toString())
                .addQueryParameter("type", "single")
                .addQueryParameter("id", txtId)
                .build()

            Log.i("ENTRY", httpUrl.toString())

            val request = Request.Builder()
                .url(httpUrl)
                .build()

            try {
                var res = ""
                client.newCall(request).enqueue(object : Callback {
                    override fun onFailure(call: Call, e: IOException) {
                        Log.i("ENTRY", "onFailure: ${e.message!!}")
                    }

                    override fun onResponse(call: Call, response: Response) {
                        res = response.body!!.string()
                        Log.i("ENTRY", "onResponse: $res")
                        val json = JSONObject(res)
                        val text = json.getString("text")

                        // Run on UI thread
                        (context as Activity).runOnUiThread {
                            createPopupDialog(text)
                        }

                    }
                })
            } catch (e: Exception) {
                Log.i("ENTRY", "onFailure: ${e.message!!}")
            }
        }

        fun createPopupDialog(text : String) {
            val dialogBuilder = AlertDialog.Builder(context)
            val inflater = context.getSystemService(Context.LAYOUT_INFLATER_SERVICE) as LayoutInflater
            val viewPopUp = inflater.inflate(R.layout.popup_entry, null)

            var popupTitle = viewPopUp.findViewById<TextView>(R.id.popup_title)
            popupTitle.text = txtTitle.text.toString()
            var popupEntry = viewPopUp.findViewById<TextView>(R.id.popup_text)
            popupEntry.text = text

            var popupSentiment = viewPopUp.findViewById<TextView>(R.id.popup_sentiment)
            popupSentiment.text = txtSentiment.text.toString()
            var popupClose = viewPopUp.findViewById<ImageView>(R.id.popup_close)

            dialogBuilder.setView(viewPopUp)
            dialog = dialogBuilder.create()
            dialog.show()

            popupClose.setOnClickListener {
                dialog.dismiss()
            }
        }
    }

}

