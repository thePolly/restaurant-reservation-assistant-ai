### Issue 1: spaCy does not reliably detect names

**Problem:**  
I tried to use spaCy to detect and mask personal names in email text, but it did not reliably recognize names in my test cases.

**What I tried:**  
- Tested spaCy on my email input  
- Checked the output entities  

**Solution / Next step:**  
I decided not to rely only on spaCy. I will extract the name from the sender metadata or use an LLM if needed.

**Takeaway:**  
spaCy is not always reliable for real-world text, so fallback solutions are needed.
