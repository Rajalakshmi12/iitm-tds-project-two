import tiktoken

encoding = tiktoken.get_encoding("cl100k_base")
prompt = """List only the valid English words from these: IgwsJe6A, EnDFTY, g, JOPp6dLM7, kY, z9eQ0, kqvIovXz, 6xCz6WN9, Qy, ue, Hkk, P, idv8VX, IYkm1IdgxZ, XLVkWpJ, PA8, TnPEW, fLWKD, zC7yHUc, uOewAPoX, o6, 2, bbWp, h, e5H, yMeSfoqI, lNgOfG, eFHQox7, fvThW4HV2f, X3Zq, Hij, i41CY, HQO9YlmP, 6zxf3huQ, z, 2NKhmE8C, h, 4n, rXm1M6LR, 7eyC7UKj, pxRMAP, nZZBRQGaRc, 3QdpgnH9, Cy, lA, moDDK, OmBQ, dDjhMZ, Ea5BHrNyg, 3uskK, av, Oobg, R1G, IOE6H, 7, cu, d, j, LcOxAfW93w, 5KYvzXc6, sa2h, EJZu, YU, exA2g, BBZWs, stQeMiOPk, Q, gZv94Ct6X4, KeS, k2oRFhR, fluQT, ZAmFk6Q, 2wp5bU, vJj, ALZAGzUp, 4jZEGZns, lBdECVPn, RObYbgNBh, nFnC19P, WI4C8o9, tuNQWDdDN"""

tokens = encoding.encode(prompt)
print(tokens)
print(len(tokens))
