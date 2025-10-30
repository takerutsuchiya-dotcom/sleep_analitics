javascript:(async () => {
  try {
    const stream = await navigator.mediaDevices.getDisplayMedia({ video: true });
    const track = stream.getVideoTracks()[0];
    const imageCapture = new ImageCapture(track);
    const bitmap = await imageCapture.grabFrame();
    const canvas = document.createElement('canvas');
    canvas.width = bitmap.width;
    canvas.height = bitmap.height;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(bitmap, 0, 0);
    const base64 = canvas.toDataURL('image/png');
    track.stop();
    const res = await fetch("http://127.0.0.1:8000/upload", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ image: base64 }),
    });
    const data = await res.json();
    alert("解析完了！結果ページに出力します。");
    window.open("index.html?report=" + encodeURIComponent(data.report));
  } catch (e) {
    alert("スクリーンショット取得に失敗しました: " + e);
  }
})();