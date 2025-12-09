import { createClient } from "@supabase/supabase-js";

export const supabaseUrl = "https://edhasunsosidmqxhyubr.supabase.co";
const supabaseKey = "sb_publishable_Jcj7E0R6yf6jdNl-RSrk_Q_z0_hQ19Y";
const supabase = createClient(supabaseUrl, supabaseKey);

export default supabase;
