package java_testcases.junit;


/**
 * Methods to format the output from the subject programs.
 * 
 * @author Matias Martinez
 *
 */

public class QuixFixOracleHelper {

	public static String format(Object out, boolean cutDecimal) {
		String r = "[";
		Object jsonOutObtained = transformToString(out, cutDecimal);
		r = r.trim().substring(0, r.length() - 1);
		String obtained = removeSymbols(jsonOutObtained.toString());
		return obtained;
	}

	public static String removeSymbols(String r) {

		r = r.replaceAll("\\(", "[").replaceAll("\\)", "]").replace(" ", "").replaceAll("\"", "");
		String s = "";
		return r;
	}

	public static String transformToString(Object out, boolean mustRemoveDecimal) {
		if (out instanceof Iterable) {
			String s = "";
			if (out instanceof Iterable)
				s = (mustRemoveDecimal && out.toString().endsWith(".0")
						? out.toString().substring(0, out.toString().length() - 2)
						: out.toString());
			else {
				s = (mustRemoveDecimal && out.toString().endsWith(".0")
						? out.toString().substring(0, out.toString().length() - 2)
						: out.toString());
			}
			return s;
		} else {
			String s = "";
			if (out instanceof Iterable)
				s += out.toString();
			else {
				s += out.toString();
			}
			return s;
		}

	}

	public static boolean isInteger(String s) {
		boolean isValidInteger = false;
		try {
			Integer.parseInt(s);
			isValidInteger = true;
		} catch (NumberFormatException ex) {
		}

		return isValidInteger;
	}
}
