package com.smeds.cloudcomputingproject

import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView

class EntryRecyclerAdapter (context: Context, entry : List<DiaryEntry>) :
    RecyclerView.Adapter<EntryRecyclerAdapter.DiaryEntryHolder>() {

    var context = context
    var entry = entry
    lateinit var listener : EntryClickListener

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): DiaryEntryHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.diary_list_items, parent, false)
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

        init {
            txtDate = itemView.findViewById(R.id.textView_date_data)
            txtTitle = itemView.findViewById(R.id.textView_title_data)
            txtSentiment = itemView.findViewById(R.id.textview_sentiment_data)
        }

        fun setDetails(entry : DiaryEntry) {
            //txtDate.text = entry.date
            txtTitle.text = entry.title
            txtSentiment.text = entry.sentiment.toString()
        }

        override fun onClick(v: View) {
            listener.onItemClick(v, txtId)
        }
    }

}

