package com.javatechig.feedreader;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import android.app.Activity;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.ListView;
import android.widget.ProgressBar;
import com.javatechig.feedreader.model.FeedItem;
//import android.support.v4.app.NotificationCompat;
//import android.support.v4.app.NotificationManagerCompat;
//import android.support.v4.app.NotificationCompat.WearableExtender;

public class FeedListActivity extends Activity {

	private ArrayList<FeedItem> feedList = null;
	private ProgressBar progressbar = null;
	private ListView feedListView = null;
	
	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_posts_list);
		progressbar = (ProgressBar) findViewById(R.id.progressBar);

        /*
        int notificationId = 001;
        Intent viewIntent = new Intent(this, ViewEventActivity.class);
        viewIntent.putExtra(EXTRA_EVENT_ID, eventId);
        PendingIntent viewPendingIntent = PendingIntent.getActivity(this, 0, viewIntent, 0);

        NotificationCompat.Builder notificationBuilder = new NotificationCompat.Builder(this)
                .setSmallIcon(R.drawable.notification_icon) .setContentTitle("My notification")
                .setContentText("Hello World!");

        NotificationManagerCompat notificationManager = NotificationManagerCompat.from(this);

        notificationManager.notify(notificationId, notificationBuilder.build());
        */

		String url = "http://app.crunchyapp.com/api/last_news_list/";
		new DownloadFilesTask().execute(url);
	}

	public void updateList() {
		feedListView= (ListView) findViewById(R.id.custom_list);
		feedListView.setVisibility(View.VISIBLE);
		progressbar.setVisibility(View.GONE);
		
		feedListView.setAdapter(new CustomListAdapter(this, feedList));
		feedListView.setOnItemClickListener(new OnItemClickListener() {

			@Override
			public void onItemClick(AdapterView<?> a, View v, int position,	long id) {
				Object o = feedListView.getItemAtPosition(position);
				FeedItem newsData = (FeedItem) o;
				
				Intent intent = new Intent(FeedListActivity.this, FeedDetailsActivity.class);
				intent.putExtra("feed", newsData);
				startActivity(intent);
			}
		});
	}

	private class DownloadFilesTask extends AsyncTask<String, Integer, Void> {

		@Override
		protected void onProgressUpdate(Integer... values) {
		}

		@Override
		protected void onPostExecute(Void result) {
			if (null != feedList) {
				updateList();
			}
		}

		@Override
		protected Void doInBackground(String... params) {
			String url = params[0];

			// getting JSON string from URL
			JSONObject json = getJSONFromUrl(url);
            Log.i("api result:",json.toString());

			//parsing json data
			parseJson(json);
			return null;
		}
	}

	
	public JSONObject getJSONFromUrl(String url) {
		InputStream is = null;
		JSONObject jObj = null;
		String json = null;

		// Making HTTP request
		try {
			// defaultHttpClient
			DefaultHttpClient httpClient = new DefaultHttpClient();
            HttpGet httpget = new HttpGet(url);
            httpget.addHeader("Authorization", "Token a4f9863905788d9e08db6003c1dcb91e45955beb");

			HttpResponse httpResponse = httpClient.execute(httpget);
			HttpEntity httpEntity = httpResponse.getEntity();
			is = httpEntity.getContent();

			BufferedReader reader = new BufferedReader(new InputStreamReader(
					is, "iso-8859-1"), 8);
			StringBuilder sb = new StringBuilder();
			String line = null;
			while ((line = reader.readLine()) != null) {
				sb.append(line + "\n");
			}
			is.close();
			json = sb.toString();
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		} catch (ClientProtocolException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}

		try {
			jObj = new JSONObject(json);
		} catch (JSONException e) {
			Log.e("JSON Parser", "Error parsing data " + e.toString());
		}

		// return JSON String
		return jObj;

	}

	public void parseJson(JSONObject json) {
		try {

			// parsing json object
			if (json.getString("status").equalsIgnoreCase("ok")) {

				//JSONArray posts = json.getJSONArray(json.toString());

                /*
				feedList = new ArrayList<FeedItem>();


				for (int i = 0; i < 5; i++) {
					JSONObject post = (JSONObject) posts.getJSONObject(i);
					FeedItem item = new FeedItem();
					item.setTitle(post.getString("title"));
					item.setDate("fecha");
					item.setId(post.getString("id"));
					item.setUrl(post.getString("url"));
					item.setContent(post.getString("content"));
					JSONArray attachments = post.getJSONArray("attachments");

					if (null != attachments && attachments.length() > 0) {
						JSONObject attachment = attachments.getJSONObject(0);
						if (attachment != null)
							//item.setAttachmentUrl(attachment.getString("url"));
                            item.setAttachmentUrl("http://placehold.it/350x150");
					}

					feedList.add(item);
				}
				*/
			}
		} catch (JSONException e) {
			e.printStackTrace();
		}
	}

}
