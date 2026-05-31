"""
TaniLink Agent Tools
"""

from datetime import datetime
from langchain_core.tools import tool


@tool
def add_produce_listing(
    phone: str,
    produce_name: str,
    quantity_kg: float,
    price_per_kg: float | None = None,
    location: str | None = None,
) -> str:
    """Save a farmer's produce listing. Call when farmer wants to sell."""
    print(f"[DB] Saving listing: {produce_name} {quantity_kg}kg from {phone}")
    return (
        f"✅ Listing berhasil disimpan!\n"
        f"Produk: {produce_name} | {quantity_kg}kg\n"
        f"Pembeli akan segera diberitahu!\n\n"
        f"✅ Saved: {produce_name} {quantity_kg}kg. Buyers will be notified!"
    )


@tool
def get_available_produce(produce_name: str | None = None) -> str:
    """Get available produce listings. Call when buyer asks what's available."""
    # In production, this queries the database
    return (
        "🌾 *Stok Tersedia / Available Stock:*\n"
        "• *Tomat* — 50kg | Rp 8.000/kg | 📍Brebes\n"
        "• *Cabai Merah* — 20kg | Rp 35.000/kg | 📍Magelang\n"
        "• *Bayam* — 15kg | Harga nego | 📍Bogor\n\n"
        "Reply nama produk untuk info lebih lanjut!"
    )


@tool
def notify_buyers(produce_name: str, quantity_kg: float, farmer_phone: str) -> str:
    """Notify subscribed buyers about new produce availability."""
    print(f"[Notif] Notifying buyers about {produce_name} {quantity_kg}kg")
    return f"✅ Buyers notified about {produce_name} {quantity_kg}kg."


@tool
def get_price_suggestion(produce_name: str, quantity_kg: float) -> str:
    """Suggest fair market price based on historical data."""
    # In production, this queries price history from database
    prices = {
        "tomat": 8000, "cabai": 35000, "bayam": 5000,
        "kangkung": 4000, "wortel": 12000, "bawang": 25000,
    }
    key = produce_name.lower()
    if key in prices:
        avg = prices[key]
        return (
            f"💰 *Rekomendasi Harga {produce_name.title()}:*\n"
            f"Rata-rata pasar: Rp {avg:,}/kg\n"
            f"Kisaran: Rp {int(avg*0.8):,} – Rp {int(avg*1.2):,}/kg\n\n"
            f"💰 Suggested: Rp {avg:,}/kg (market average)"
        )
    return (
        f"Belum ada data harga untuk {produce_name}.\n"
        f"Cek harga pasar lokal ya!\n\n"
        f"No price data for {produce_name} yet."
    )
