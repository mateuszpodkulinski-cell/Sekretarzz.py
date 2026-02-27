import discord, asyncio, io, os
from discord.ext import commands
from datetime import datetime

# ==============================
# CONFIG
# ==============================
TOKEN = "MTQ2Njg1NTA2MTMyOTAxOTAxNQ.G5jqmk.jzDTxVq20Hb_CU8gdebhxUiAvoPxLs6_Ep6nIY"
ID_KATEGORII_TICKETOW = 1466852506247369108
CHANNEL_TICKET_PANEL = 1452677453377044572
CHANNEL_LOG_TICKET = 1466852664372494597
URL_LOGO_IRL = "https://i.imgur.com/ZJS6TRT.jpeg"
URL_IMG_PANEL = "https://i.imgur.com/7iYt1yN.jpeg"

# ==============================
def sc(text):
    trans = str.maketrans(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘqʀꜱᴛᴜᴠᴡxʏᴢABCDEFGHIJKLMNOPQRSTUVWXYZ"
    )
    return str(text).translate(trans)

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        self.add_view(TicketView())
        self.add_view(AdminTicketActions())
        # ReactionRoleView została usunięta, bo nie była zdefiniowana

bot = MyBot()

# --- ADMIN ACTIONS ---
class AdminTicketActions(discord.ui.View):
    def __init__(self): super().__init__(timeout=None)

    @discord.ui.button(label=sc("ᴘʀᴢʏᴊᴍɪᴊ"), style=discord.ButtonStyle.green, custom_id="adm_take_v6")
    async def take(self, it: discord.Interaction, btn: discord.ui.Button):
        if not it.user.guild_permissions.administrator: return
        e = discord.Embed(
            description=f"{sc('ᴢɢᴌᴏꜱᴢᴇɴɪᴇ ᴢᴏꜱᴛᴀɴɪᴇ ʀᴏᴢᴘᴀᴛʀᴢᴏɴᴇ ᴘʀᴢᴇᴢ')} {it.user.mention}",
            color=0x2ecc71
        )
        btn.disabled = True
        btn.label = sc("ᴘʀᴢʏᴊᴇ̨ᴛᴇ")
        await it.response.edit_message(view=self)
        await it.channel.send(embed=e)

    @discord.ui.button(label=sc("ᴢᴀᴍᴋɴɪᴊ"), style=discord.ButtonStyle.red, custom_id="adm_close_v6")
    async def close(self, it: discord.Interaction, btn: discord.ui.Button):
        if not it.user.guild_permissions.administrator: return

        emb = discord.Embed(title=sc("ᴢᴀᴍʏᴋᴀɴɪᴇ ᴛɪᴄᴋᴇᴛᴜ"), color=0xff0000)
        await it.response.send_message(embed=emb)
        msg = await it.original_response()

        for i in range(10, -1, -1):
            emb.description = sc(f"ᴢɢᴌᴏꜱᴢᴇɴɪᴇ ᴢᴏꜱᴛᴀɴɪᴇ ᴢᴀᴍᴋɴɪᴇ̨ᴛᴇ ᴢᴀ: {i}...")
            await msg.edit(embed=emb)
            await asyncio.sleep(1)

        log_ch = it.guild.get_channel(CHANNEL_LOG_TICKET)
        log_txt = f"ʟᴏɢ ᴛɪᴄᴋᴇᴛᴜ: {it.channel.name.upper()}\n"

        async for m in it.channel.history(limit=None, oldest_first=True):
            log_txt += f"[{m.created_at.strftime('%H:%M')}] {m.author.display_name.upper()}: {m.content}\n"

        if log_ch:
            file = discord.File(io.BytesIO(log_txt.encode()), filename=f"log-{it.channel.name}.txt")
            le = discord.Embed(
                title=sc("ᴛɪᴄᴋᴇᴛ ᴢᴀᴍᴋɴɪᴇ̨ᴛʏ"),
                color=0xe67e22,
                timestamp=datetime.now()
            )
            le.add_field(name=sc("ᴋᴀɴᴀᴌ"), value=sc(it.channel.name))
            le.add_field(name=sc("ᴢᴀᴍᴋɴᴀ̨ᴌ"), value=it.user.mention)
            await log_ch.send(embed=le, file=file)

        await it.channel.delete()

# --- TICKET PANEL ---
class TicketView(discord.ui.View):
    def __init__(self): super().__init__(timeout=None)

    @discord.ui.button(label=sc("ᴘᴏᴍᴏᴄ"), style=discord.ButtonStyle.primary, custom_id="p1")
    async def p1(self, it, b): await it.response.send_modal(HelpModal())

    @discord.ui.button(label=sc("ꜱᴏᴊᴜꜱᴢ"), style=discord.ButtonStyle.success, custom_id="p2")
    async def p2(self, it, b): await it.response.send_modal(AllModal())

    @discord.ui.button(label=sc("ᴄᴢᴌᴏɴᴋᴏꜱᴛᴡᴏ"), style=discord.ButtonStyle.secondary, custom_id="p3")
    async def p3(self, it, b): await it.response.send_modal(MemModal())

# --- FORMULARZE ---
class HelpModal(discord.ui.Modal, title=sc("ᴘᴏᴍᴏᴄ")):
    n = discord.ui.TextInput(label=sc("ɴɪᴄᴋ"))
    o = discord.ui.TextInput(label=sc("ᴏᴘɪꜱ"), style=discord.TextStyle.paragraph)

    async def on_submit(self, it):
        await finalize_ticket(it, "ᴘᴏᴍᴏᴄ", {
            "ɴɪᴄᴋ": self.n.value,
            "ᴏᴘɪꜱ": self.o.value
        })

class AllModal(discord.ui.Modal, title=sc("ꜱᴏᴊᴜꜱᴢ")):
    n = discord.ui.TextInput(label=sc("ᴘʀᴇᴢʏᴅᴇɴᴛ"))
    p = discord.ui.TextInput(label=sc("ɴᴀᴢᴡᴀ ᴘᴀɴ́ꜱᴛᴡᴀ"))
    o = discord.ui.TextInput(label=sc("ᴏᴘɪꜱ"), style=discord.TextStyle.paragraph)
    f = discord.ui.TextInput(label=sc("ᴏꜰᴇʀᴛᴀ"), style=discord.TextStyle.paragraph)

    async def on_submit(self, it):
        await finalize_ticket(it, "ꜱᴏᴊᴜꜱᴢ", {
            "ᴘʀᴇᴢʏᴅᴇɴᴛ": self.n.value,
            "ᴘᴀɴ́ꜱᴛᴡᴏ": self.p.value,
            "ᴏᴘɪꜱ": self.o.value,
            "ᴏꜰᴇʀᴛᴀ": self.f.value
        })

class MemModal(discord.ui.Modal, title=sc("ᴄᴢᴌᴏɴᴋᴏꜱᴛᴡᴏ")):
    n = discord.ui.TextInput(label=sc("ɴɪᴄᴋ"))
    w = discord.ui.TextInput(label=sc("ᴡɪᴇᴋ"))
    d = discord.ui.TextInput(label=sc("ᴏᴘɪꜱ ꜱɪᴇʙɪᴇ"), style=discord.TextStyle.paragraph)
    r = discord.ui.TextInput(label=sc("ᴄᴢʏ ᴘʀᴢᴇᴄᴢʏᴛᴀᴌᴇꜱ́ ʀᴇɢᴜʟᴀᴍɪɴ?"))

    async def on_submit(self, it):
        await finalize_ticket(it, "ᴄᴢᴌᴏɴᴋᴏꜱᴛᴡᴏ", {
            "ɴɪᴄᴋ": self.n.value,
            "ᴡɪᴇᴋ": self.w.value,
            "ᴏᴘɪꜱ": self.d.value,
            "ʀᴇɢᴜʟᴀᴍɪɴ": self.r.value
        })

# ==============================
# FINALIZE_TICKET – DUŻY NAGŁÓWEK W TREŚCI
# ==============================
async def finalize_ticket(it, name, fields):
    cat = it.guild.get_channel(ID_KATEGORII_TICKETOW)
    ch = await it.guild.create_text_channel(f"{name}-{it.user.name}", category=cat)

    await ch.set_permissions(it.guild.default_role, view_channel=False)
    await ch.set_permissions(it.user, view_channel=True, send_messages=True)

    if name == "ᴘᴏᴍᴏᴄ":
        header = "ᴄᴇɴᴛʀᴜᴍ ᴘᴏᴍᴏᴄʏ"
        footer = "ɪʀʟ - ᴄᴇɴᴛʀᴜᴍ ᴘᴏᴍᴏᴄʏ"
    elif name == "ꜱᴏᴊᴜꜱᴢ":
        header = "ᴄᴇɴᴛʀᴜᴍ ꜱᴏᴊᴜꜱᴢᴜ"
        footer = "ɪʀʟ - ᴄᴇɴᴛʀᴜᴍ ꜱᴏᴊᴜꜱᴢᴜ"
    else:
        header = "ᴄᴇɴᴛʀᴜᴍ ᴄᴢᴌᴏɴᴋᴏꜱᴛᴡᴀ"
        footer = "ɪʀʟ - ᴄᴇɴᴛʀᴜᴍ ᴄᴢᴌᴏɴᴋᴏꜱᴛᴡᴀ"

    e = discord.Embed(color=0x3498db)
    e.set_thumbnail(url=URL_LOGO_IRL)

    desc = f"# {header}\n\n"
    desc += "```\n"
    for k, v in fields.items():
        desc += f"{k}: {v}\n"
    desc += "```"
    desc += f"\n*{footer}*"

    e.description = desc
    await ch.send(it.user.mention, embed=e, view=AdminTicketActions())
    await it.response.send_message(sc("ᴢɢᴌᴏꜱᴢᴇɴɪᴇ ᴏᴛᴡᴀʀᴛᴇ"), ephemeral=True)

# --- KOMENDA TICKET ---
@bot.tree.command(name="ticket", description="Wysyła panel ticketów")
async def slash_tic(it: discord.Interaction):
    await it.response.send_message(sc("ᴡʏꜱʏᴌᴀɴɪᴇ..."), ephemeral=True)
    e = discord.Embed(
        description=f"# {sc('ᴄᴇɴᴛʀᴜᴍ ᴢɢᴌᴏꜱᴢᴇɴ́ ɪʀʟ')}\n\n"
                    f"{sc('ᴀʙʏ ꜱᴛᴡᴏʀᴢʏᴄ́ ᴢɢᴌᴏꜱᴢᴇɴɪᴇ ᴋʟɪᴋɴɪᴊ ɴᴀ ᴊᴇᴅᴇɴ ᴢ ᴘᴏɴɪᴢ̇ꜱᴢʏᴄʜ ᴘʀᴢʏᴄɪꜱᴋᴏ́ᴡ')}",
        color=0x2f3136
    )
    e.set_image(url=URL_IMG_PANEL)
    e.set_footer(text=sc("ɪʀʟ - ᴄᴇɴᴛʀᴜᴍ ᴢɢᴌᴏꜱᴢᴇɴ́"))
    await it.channel.send(embed=e, view=TicketView())

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot 2026 gotowy: {bot.user}")

    ch = bot.get_channel(CHANNEL_TICKET_PANEL)
    if ch:
        await ch.purge(limit=10)
        e = discord.Embed(
            description=f"# {sc('ᴄᴇɴᴛʀᴜᴍ ᴢɢᴌᴏꜱᴢᴇɴ́ ɪʀʟ')}\n\n"
                        f"{sc('ᴀʙʏ ꜱᴛᴡᴏʀᴢʏᴄ́ ᴢɢᴌᴏꜱᴢᴇɴɪᴇ ᴋʟɪᴋɴɪᴊ ɴᴀ ᴊᴇᴅᴇɴ ᴢ ᴘᴏɴɪᴢ̇ꜱᴢʏᴄʜ ᴘʀᴢʏᴄɪꜱᴋᴏ́ᴡ')}",
            color=0x2f3136
        )
        e.set_image(url=URL_IMG_PANEL)
        e.set_footer(text=sc("ɪʀʟ - ᴄᴇɴᴛʀᴜᴍ ᴢɢᴌᴏꜱᴢᴇɴ́"))
        await ch.send(embed=e, view=TicketView())

bot.run("MTQ2Njg1NTA2MTMyOTAxOTAxNQ.G5jqmk.jzDTxVq20Hb_CU8gdebhxUiAvoPxLs6_Ep6nIY")
