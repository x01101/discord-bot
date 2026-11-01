import os
import discord
from discord.ext import commands
from discord import app_commands

# إعداد الصلاحيات (Intents) اللازمة للبوت
intents = discord.Intents.default()
intents.voice_states = True  # مهم جداً للتعامل مع الرومات الصوتية
intents.message_content = True

# تعريف البوت
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} (ID: {bot.user.id})")
    try:
        # مزامنة أوامر السلاش (Slash Commands) مع ديسكورد
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s).")
    except Exception as e:
        print(e)

# تصميم أمر السلاش /setup لجعل البوت يدخل روم صوتي محدد بالـ ID
@bot.tree.command(name="setup", description="أمر لجعل البوت يدخل روم صوتي محدد عبر الـ ID")
@app_commands.describe(channel_id="اكتب آي دي روم الفويس هنا")
async def setup(interaction: discord.Interaction, channel_id: str):
    # التحقق من أن الكود يحتوي على أرقام فقط
    if not channel_id.isdigit():
        await interaction.response.send_message("❌ آي دي الروم غير صحيح، تأكد أنه أرقام فقط!", ephemeral=True)
        return

    channel = bot.get_channel(int(channel_id))

    # التحقق من أن الروم موجود وأنه روم صوتي (Voice Channel)
    if isinstance(channel, discord.VoiceChannel):
        try:
            # محاولة الدخول للروم الصوتي
            await channel.connect()
            await interaction.response.send_message(f"✅ تم الانضمام بنجاح إلى الروم: **{channel.name}**", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ حدث خطأ أثناء محاولة الدخول: {e}", ephemeral=True)
    else:
        await interaction.response.send_message("❌ لم يتم العثور على الروم الصوتي بهذا الآي دي، تأكد أنه روم صوتي وليس كتابي!", ephemeral=True)

# تشغيل البوت باستخدام متغيرات البيئة (آمن جداً للاستضافة و GitHub)
# (إذا كنت تجربه محلياً في VS Code، يمكنك استبدال os.getenv("DISCORD_TOKEN") بالتوكن المباشر بين علامتي تنصيص)
bot.run(os.getenv("MTU2NjM2NzY5MjE3OTY0MDM3MA.GXe3OT.Bry2z-d6sFTVj2sAWpjdHmTlN6NOMycKWVXZow"))