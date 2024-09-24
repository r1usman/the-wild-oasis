import { createClient } from "@supabase/supabase-js";

export const supabaseUrl = "https://edhasunsosidmqxhyubr.supabase.co";
const supabaseKey =
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVkaGFzdW5zb3NpZG1xeGh5dWJyIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTQzNjU4NTMsImV4cCI6MjAwOTk0MTg1M30.xW3MPoJzyZKVJ9zo1PviWyjVMJUuSS51D_0g4D36how";
const supabase = createClient(supabaseUrl, supabaseKey);

export default supabase;
