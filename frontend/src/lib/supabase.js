import { createClient } from '@supabase/supabase-js';

// Vite requires the VITE_ prefix
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL?.trim();
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY?.trim();

// Avoid crashing the whole app immediately; log a clear error instead
if (!supabaseUrl || !supabaseAnonKey) {
  console.error("⚠️ Supabase: Missing VITE_SUPABASE_URL or VITE_SUPABASE_ANON_KEY in .env");
}

export const supabase = createClient(
  supabaseUrl || 'https://placeholder.supabase.co', 
  supabaseAnonKey || 'placeholder-key'
);