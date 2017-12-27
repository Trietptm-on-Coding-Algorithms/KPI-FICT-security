import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public class Decryptor {

	private String text;
	private float quality;
	private Map<String, Float> trigram;
	private Map<String, String> key = new LinkedHashMap<String, String>() {
	{
		put("A", "A");
		put("B", "B");
		put("C", "C");
		put("D", "D");
		put("E", "E");
		put("F", "F");
		put("G", "G");
		put("H", "H");
		put("I", "I");
		put("J", "J");
		put("K", "K");
		put("L", "L");
		put("M", "M");
		put("N", "N");
		put("O", "O");
		put("P", "P");
		put("Q", "Q");
		put("R", "R");
		put("S", "S");
		put("T", "T");
		put("U", "U");
		put("V", "V");
		put("W", "W");
		put("X", "X");
		put("Y", "Y");
		put("Z", "Z");
	}};

	private List<String> alphabet = new ArrayList<String>() {
	{	
		add("A"); add("B");	add("C"); add("D"); add("E"); add("F");
		add("G"); add("H"); add("I"); add("J"); add("K"); add("L");
		add("M"); add("N"); add("O"); add("P"); add("Q"); add("R");
		add("S"); add("T"); add("U"); add("V"); add("W"); add("X");
		add("Y"); add("Z");
	}};

	public Decryptor(String text) {
		this.quality = -999999;
		this.text = text;
		this.trigram = FileWorker.loadTrigram();
	}

	protected String decrypt(String encryptedText, Map<String, String> currentKey) {
		String currDecryptedText = new String("");
		for (int i = 0; i < encryptedText.length(); i++) {
			currDecryptedText += currentKey.get(Character.toString(encryptedText.charAt(i)));
		}
		return currDecryptedText;
	}

	protected float computeQuality(String text) {
		float currentQuality = 0;
		for (int i = 0; i < text.length() - 3 + 1; i++) {
			if (this.trigram.containsKey(text.substring(i, i + 3)))
				currentQuality += this.trigram.get(text.substring(i, i + 3));
		}
		return currentQuality;
	}

	public String attack_crypt() {
		String decryptedText = "";
		int i = 0;
		while (i < 1111) {
			Map<String, String> currentKey = this.changeKey();
			String currentText = decrypt(text, currentKey);

			float currentQuality = computeQuality(currentText);
			if (currentQuality > this.quality) {
				this.quality = currentQuality;
				this.key = currentKey;
				System.out.println(this.quality);
				System.out.println(this.key);
				decryptedText = currentText;
				i = 0;
			}
			i++;
		}
		return decryptedText;
	}

	private Map<String, String> changeKey()
	{
		Map<String, String> currentKey = new LinkedHashMap<>(this.key);
		int letterPosition1 = (int) (Math.random() * 26);
		int letterPosition2 = (int) (Math.random() * 26);
		
		String a = currentKey.get(alphabet.get(letterPosition2));
		String b = currentKey.get(alphabet.get(letterPosition1));
		
		currentKey.put(alphabet.get(letterPosition1), a);
		currentKey.put(alphabet.get(letterPosition2), b);				
		return currentKey;
	}

	public void printKey() {
		for (Map.Entry<String, String> entry: key.entrySet()) {
			System.out.println(entry.getKey() + ": " + entry.getValue());
		}
	}
	
}
