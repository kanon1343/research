package java_testcases.junit;


/**
 * Methods to format the output from the subject programs.
 * 
 * @author Matias Martinez
 *
 */

public class QuixFixOracleHelper {

	public static String format(Object out, boolean cutDecimal) {
		Object jsonOutObtained = transformToString(out, cutDecimal);
		String obtained = removeSymbols(jsonOutObtained.toString());
		return obtained;
	}

	public static String removeSymbols(String r) {

		r = r.replaceAll("\\(", "[").replaceAll("\\)", "]").replace(" ", "").replaceAll("\"", "");
		return r;
	}

	public static String transformToString(Object out, boolean mustRemoveDecimal) {
		if (out instanceof Iterable) {
			String r = "[";
			for (Object o : (Iterable) out) {
				r += transformToString(o, mustRemoveDecimal) + ",";
			}
			if (out instanceof Iterable) {
			}

			{
				String s = "";
				if (out instanceof String && !isInteger(out.toString()))
					s += out.toString();
				else {
					s += out.toString();
					s = (mustRemoveDecimal && out.toString().endsWith(".0")
							? out.toString().substring(0, out.toString().length() - 2)
							: out.toString());
					for (Object o:(Iterable)out){}
				}
				return s;
			}
		} else {
			String s = "";
			s = (mustRemoveDecimal && out.toString().endsWith(".0")
					? out.toString().substring(0, out.toString().length() - 2)
					: out.toString());
			if (out instanceof String && !isInteger(out.toString()))
				s += out.toString();
			else {
			}
			s += out.toString();
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
