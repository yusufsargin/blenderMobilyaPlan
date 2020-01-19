# BlenderMobilyaPlan

- Projemizin amacı kullanıcıların (www.mobilyaplan.com) sitemizde çizdikleri çizimlerin
3d ve gerçekci renderını alabilmelerini sağlamaktır.
- Blender üzerinden geliştirdiğimiz sistem sayesinde müşteriler internette çizdikleri SVG çizimlerin
Render görüntülerini dakikalar içerisinde kendilene mail olarak alabileceklerdir.

# Program Çalışma Mantığı

- İnternet sitemizde çizilen çizimler ara servis aracılığı ile blender'a gelmektedir. Gelen
çizimlerin datalarına göre Blender üzrinde çizimi yapılmaktadır. Yapılan çizimler yine siteden
Gönderilen texture  kodları ile UvMap yapılarak giydirilmektedir. Üzerinde bump ve normal mapler
blender tarafından üretilmektedir. Buna göre Cycle üzerinde 120 sample ile render alınmaktadır.
Alınan render ortalama süresi 30sn-1 dk arasında değişmektedir. Program kendi içerisinde her 
20 saniyede Database'i tetiklemektedir. Böyledece program render yaparken Database kaydedilen
çizimler için veriliş zamanına göre bir kuyruk oluşturur. Burada blender'ın event based
yapısı kullanılmıştır. Renderı biten çizim gönderen kişini mail adresine gmail üzerine yazılan bir
servis ile  gönderilir. Render olan üyeler Database üzerine kaydedilmekte. Böylece arada 
yazdığımız serviste müşterilerin render sayılarına göre maliyet  hesabı yapılmaktadır. Arada çıkabilecek
arızalar yazdığımız test sistemi sayesinde yakalanıp bize blender (.blend) formatında mail atılmaktadır.
Böylece müşterinin yaşadığı sıkıntı kolayca giderilebilmektedir.  Yazdığımız ara servisde 
müşteriye ulaşılarak hatası giderilebilecektir.

# Sektörde yeri

- Yaptığımız pazar analizlerinde ve üyelerimiz olan yaklaşık 120 mobilyacı üzerinden topladığımız verilere
göre sistem mimarlar, üreticiler ve dekorasyoncular için kapıtılacak büyük bir eksikliktir.
- Programımız sayesinde sadece dakikalar içerisinde komplex bir mutfak çizilip oda içerisinde render
görüntüleri alınabilecektir.

# Render Görüntürlerden Örnekler

- Sistem den çıkan renderlar şuan test aşamasındadır. Texture kütüphanesine yeni textureler eklendikce
Kalite dahada artmaktadır.


![render](https://firebasestorage.googleapis.com/v0/b/blender-44440.appspot.com/o/MobilyaPlan_CustomerName.png?alt=media&token=5e1256a8-e48c-4dce-ab14-5d379b561102)

- Web sitesi (www.mobilyaplan.com) SVG çizim 

![SVG](https://firebasestorage.googleapis.com/v0/b/blender-44440.appspot.com/o/furniturePlan.png?alt=media&token=df2e9ecb-84d9-4d67-85ad-e90e1441ea58)