// circle8 waitlist — Google Apps Script backend
// Kurulum: Google Sheets'de yeni bir tablo aç > Extensions > Apps Script >
// bu dosyayı yapıştır > Deploy > New deployment > Web app >
//   Execute as: Me / Who has access: Anyone
// > çıkan URL'yi index.html içindeki FORM_ENDPOINT değerine yapıştır.

function doPost(e) {
  const data = JSON.parse(e.postData.contents);
  if (data.website) return json({ ok: false }); // honeypot: bot kaydı
  const sheet = getSheet();
  sheet.appendRow([
    new Date(),
    String(data.email || "").slice(0, 200),
    data.consent ? "yes" : "no",
    String(data.source || "").slice(0, 50)
  ]);
  return json({ ok: true, count: count() });
}

function doGet(e) {
  if (e && e.parameter && e.parameter.count) return json({ count: count() });
  return json({ ok: true });
}

function getSheet() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName("signups");
  if (!sheet) {
    sheet = ss.insertSheet("signups");
    sheet.appendRow(["timestamp", "email", "consent", "source"]);
  }
  return sheet;
}

function count() {
  return Math.max(0, getSheet().getLastRow() - 1);
}

function json(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
